
# Реализуйте здесь простую машину состояний (State Machine).
# Функция должна принимать текущее состояние и событие,
# и возвращать следующее состояние.

def next_state(state: str, event: str) -> str:
    transitions = {
        ("NEW", "PAY_OK"): "PAID",
        ("NEW", "PAY_FAIL"): "CANCELLED",
        ("PAY_OK", "DELIVERY_OK") : "DELIVERY",
        ("PAY_OK", "DELIVERY_FAIL") : "CANCELLED",
    }

    return transitions.get((state, event), state)