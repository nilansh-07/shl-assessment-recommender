import pytest
from core.recommender import Recommender, Assessment

def test_assessment_creation():
    """Test that Assessment objects can be created correctly"""
    assessment = Assessment(
        name="Test Assessment",
        url="https://example.com",
        remote_testing=True,
        adaptive_irt=True,
        duration="30 minutes",
        test_type="Cognitive",
        description="Test description"
    )
    
    assert assessment.name == "Test Assessment"
    assert assessment.remote_testing is True
    assert assessment.adaptive_irt is True

def test_recommender_initialization():
    """Test that the Recommender can be initialized"""
    recommender = Recommender()
    assert recommender is not None
    assert len(recommender.db.assessments) > 0

def test_get_recommendations():
    """Test that recommendations can be retrieved"""
    recommender = Recommender()
    query = "Looking for a cognitive assessment for software engineers"
    
    recommendations = recommender.get_recommendations(query, max_results=3)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 3
    for recommendation in recommendations:
        assert isinstance(recommendation, Assessment)
        assert hasattr(recommendation, 'name')
        assert hasattr(recommendation, 'url')
        assert hasattr(recommendation, 'description') 