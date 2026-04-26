from abc import ABC, abstractmethod
from datetime import datetime


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str, customer_id: str) -> dict:
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str) -> dict:
        pass


class StripeAPI:

    def create_charge(self, amount_cents: int, currency_code: str, customer_token: str) -> str:
        print(f"  📤 Stripe получил: списать {amount_cents} {currency_code} (это {amount_cents / 100} {currency_code})")
        return f"stripe_tx_{datetime.now().timestamp()}"

    def reverse_charge(self, charge_id: str) -> bool:
        print(f"  ↩️  Stripe получил: вернуть деньги за {charge_id}")
        return True


class PayPalAPI:

    def make_payment(self, amount_usd: float, payer_email: str) -> str:
        print(f"PayPal получил: списать ${amount_usd:.2f} с {payer_email}")
        return f"paypal_tx_{datetime.now().timestamp()}"

    def cancel_payment(self, payment_id: str) -> dict:
        print(f"PayPal получил: вернуть деньги за {payment_id}")
        return {"status": "cancelled"}



class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe_api: StripeAPI):
        self._stripe = stripe_api

    def process_payment(self, amount: float, currency: str, customer_id: str) -> dict:
        print(f"\nМы попросили: списать {amount} {currency}")

        amount_cents = int(amount * 100)
        print(f"Адаптер перевёл: {amount} {currency} → {amount_cents} центов")

        transaction_id = self._stripe.create_charge(amount_cents, currency, customer_id)

        return {
            "success": True,
            "transaction_id": transaction_id,
            "processor": "Stripe",
            "amount": amount,
            "currency": currency
        }

    def refund_payment(self, transaction_id: str) -> dict:
        print(f"\nМы попросили: вернуть деньги за {transaction_id[:20]}...")
        success = self._stripe.reverse_charge(transaction_id)
        return {
            "success": success,
            "transaction_id": transaction_id,
            "processor": "Stripe"
        }


class PayPalAdapter(PaymentProcessor):
    def __init__(self, paypal_api: PayPalAPI):
        self._paypal = paypal_api

    def process_payment(self, amount: float, currency: str, customer_id: str) -> dict:
        print(f"\nМы попросили: списать {amount} {currency}")

        original_amount = amount
        if currency != "USD":
            amount = amount * 1.05
            print(f"Адаптер перевёл: {original_amount} {currency} → ${amount:.2f} USD")

        transaction_id = self._paypal.make_payment(amount, customer_id)

        return {
            "success": True,
            "transaction_id": transaction_id,
            "processor": "PayPal",
            "amount": amount,
            "currency": "USD"
        }

    def refund_payment(self, transaction_id: str) -> dict:
        print(f"\nМы попросили: вернуть деньги за {transaction_id[:20]}...")
        result = self._paypal.cancel_payment(transaction_id)
        return {
            "success": result.get("status") == "cancelled",
            "transaction_id": transaction_id,
            "processor": "PayPal"
        }


if __name__ == "__main__":

    stripe_api = StripeAPI()
    paypal_api = PayPalAPI()

    stripe_adapter = StripeAdapter(stripe_api)
    paypal_adapter = PayPalAdapter(paypal_api)

    print("\n" + "─" * 60)
    print("💰 STRIPE")
    print("─" * 60)

    result1 = stripe_adapter.process_payment(99.99, "EUR", "customer_12345")
    print(f"\n  ✅ ИТОГ: Платёж {result1['amount']} {result1['currency']} прошёл!")

    refund1 = stripe_adapter.refund_payment(result1["transaction_id"])
    print(f"\n  ✅ ИТОГ: Возврат прошёл!")

    print("\n" + "─" * 60)
    print("💰 PAYPAL")
    print("─" * 60)

    result2 = paypal_adapter.process_payment(99.99, "EUR", "customer_12345")
    print(f"\n  ✅ ИТОГ: Платёж {result2['amount']:.2f} {result2['currency']} прошёл!")

    refund2 = paypal_adapter.refund_payment(result2["transaction_id"])
    print(f"\n  ✅ ИТОГ: Возврат прошёл!")

    print("\n" + "─" * 60)
    print("💰 YOOKASSA (новая платежная система)")
    print("─" * 60)


    class YooKassaAPI:
        def charge_card(self, rubles: float, card_token: str) -> str:
            print(f"  📤 YooKassa получил: списать {rubles} руб. с карты {card_token}")
            return f"yk_tx_{datetime.now().timestamp()}"

        def refund_charge(self, charge_token: str) -> bool:
            print(f"  ↩️  YooKassa получил: вернуть деньги за {charge_token}")
            return True


    class YooKassaAdapter(PaymentProcessor):
        def __init__(self, yookassa: YooKassaAPI):
            self._yookassa = yookassa

        def process_payment(self, amount: float, currency: str, customer_id: str) -> dict:
            print(f"\n  👤 Мы попросили: списать {amount} {currency}")

            if currency != "RUB":
                amount = amount * 100
                print(f"  🔄 Адаптер перевёл: в рубли")

            tx_id = self._yookassa.charge_card(amount, customer_id)
            return {"success": True, "transaction_id": tx_id, "processor": "YooKassa"}

        def refund_payment(self, transaction_id: str) -> dict:
            print(f"\n  👤 Мы попросили: вернуть деньги")
            return {"success": self._yookassa.refund_charge(transaction_id), "transaction_id": transaction_id}


    yk_adapter = YooKassaAdapter(YooKassaAPI())
    result3 = yk_adapter.process_payment(1500, "RUB", "card_98765")
    print(f"\n  ✅ ИТОГ: Платёж 1500 RUB прошёл!")

    print("\n" + "=" * 60)
    print("🎉 ВСЕ ПЛАТЕЖИ УСПЕШНО ОБРАБОТАНЫ!")
    print("=" * 60)