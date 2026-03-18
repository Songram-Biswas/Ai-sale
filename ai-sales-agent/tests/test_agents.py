from app.agents.data_collection_agent import DataCollectionAgent
from app.agents.insight_agent import InsightAgent


class _FakeCollection:
    def insert_one(self, doc):
        class _R:
            inserted_id = "fakeid"

        return _R()

    def count_documents(self, query):
        return 0


class _FakeDB(dict):
    def __getitem__(self, name):
        return _FakeCollection()


def test_data_collection_agent_runs():
    agent = DataCollectionAgent(db=_FakeDB())
    out = agent.collect("https://example.com")
    assert out["company_url"] == "https://example.com"
    assert "raw" in out
    assert "processed" in out


def test_insight_agent_runs():
    agent = InsightAgent(db=_FakeDB())
    out = agent.generate_insights({"name": "ExampleCo"})
    assert "sales_insights" in out
    assert "pain_points" in out
    assert "hooks" in out

