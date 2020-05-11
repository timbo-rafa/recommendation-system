from app.recommendation.recommendation import recommend

class RecommendationTest:
    def test_should_recommend_products_in_list(self):
        suggestions = recommend(1)

        for s in suggestions:
            pass
        pass