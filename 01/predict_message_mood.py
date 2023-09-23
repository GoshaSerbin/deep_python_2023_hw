class SomeModel:
    def predict(self, message: str) -> float:
        pass


class InvalidArguments(Exception):
    pass


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if bad_thresholds > good_thresholds:
        raise InvalidArguments(
            "bad_thresholds must be less than good_thresholds"
        )
    model_predict = model.predict(message)
    if model_predict < bad_thresholds:
        return "неуд"
    if model_predict > good_thresholds:
        return "отл"
    return "норм"
