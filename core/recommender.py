from typing import List, Dict, Optional
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Google Gemini
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    logger.error("GOOGLE_API_KEY environment variable is not set")
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

try:
    genai.configure(api_key=api_key)
    # List available models
    models = genai.list_models()
    logger.info("Available models:")
    for model in models:
        logger.info(f"- {model.name}")
    
    # Set default safety settings
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    logger.info("Google Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Google Gemini API: {str(e)}")
    logger.error(traceback.format_exc())
    raise

class Assessment(BaseModel):
    name: str
    url: str
    remote_testing: bool
    adaptive_irt: bool
    duration: str
    test_type: str
    description: str

class AssessmentDatabase:
    def __init__(self):
        self.assessments: List[Assessment] = []
        try:
            self._load_assessments()
            logger.info(f"Loaded {len(self.assessments)} assessments")
        except Exception as e:
            logger.error(f"Failed to load assessments: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def _load_assessments(self):
        try:
            # Sample assessments
            self.assessments = [
                Assessment(
                    name="OPQ32",
                    url="https://www.shl.com/assessments/opq32",
                    remote_testing=True,
                    adaptive_irt=True,
                    duration="30-40 minutes",
                    test_type="Personality",
                    description="Measures personality traits and work preferences"
                ),
                Assessment(
                    name="Verify G+",
                    url="https://www.shl.com/assessments/verify-g-plus",
                    remote_testing=True,
                    adaptive_irt=True,
                    duration="25-30 minutes",
                    test_type="Cognitive",
                    description="Measures general cognitive ability and problem-solving skills"
                ),
                Assessment(
                    name="Verify Numerical",
                    url="https://www.shl.com/assessments/verify-numerical",
                    remote_testing=True,
                    adaptive_irt=True,
                    duration="20-25 minutes",
                    test_type="Cognitive",
                    description="Measures numerical reasoning and data interpretation skills"
                ),
                Assessment(
                    name="Verify Verbal",
                    url="https://www.shl.com/assessments/verify-verbal",
                    remote_testing=True,
                    adaptive_irt=True,
                    duration="20-25 minutes",
                    test_type="Cognitive",
                    description="Measures verbal reasoning and comprehension skills"
                ),
                Assessment(
                    name="Verify Inductive",
                    url="https://www.shl.com/assessments/verify-inductive",
                    remote_testing=True,
                    adaptive_irt=True,
                    duration="20-25 minutes",
                    test_type="Cognitive",
                    description="Measures logical reasoning and pattern recognition skills"
                ),
                Assessment(
                    name="MOTIFY",
                    url="https://www.shl.com/assessments/motify",
                    remote_testing=True,
                    adaptive_irt=False,
                    duration="15-20 minutes",
                    test_type="Motivation",
                    description="Measures work motivation and preferences"
                ),
                Assessment(
                    name="Situational Judgement Test",
                    url="https://www.shl.com/assessments/situational-judgement-test",
                    remote_testing=True,
                    adaptive_irt=False,
                    duration="30-35 minutes",
                    test_type="Behavioral",
                    description="Measures decision-making and problem-solving in work scenarios"
                )
            ]
            logger.debug(f"Assessment names: {[a.name for a in self.assessments]}")
        except Exception as e:
            logger.error(f"Error loading assessments: {str(e)}")
            logger.error(traceback.format_exc())
            raise

class Recommender:
    def __init__(self):
        try:
            self.db = AssessmentDatabase()
            logger.info("Recommender initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize recommender: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def get_recommendations(self, query: str, max_results: int = 10) -> List[Assessment]:
        """
        Get assessment recommendations based on a natural language query.
        Uses an enhanced keyword matching and scoring system.
        """
        try:
            logger.info(f"Generating recommendations for query: {query}")
            query = query.lower()
            
            # Enhanced keyword mappings with weights
            keyword_categories = {
                'cognitive': {
                    'keywords': ['problem-solving', 'analytical', 'logic', 'reasoning', 'thinking', 'cognitive', 'intelligence'],
                    'weight': 3
                },
                'personality': {
                    'keywords': ['personality', 'behavior', 'traits', 'preferences', 'style', 'character', 'temperament'],
                    'weight': 2
                },
                'numerical': {
                    'keywords': ['numerical', 'mathematical', 'calculation', 'data', 'numbers', 'quantitative', 'statistics'],
                    'weight': 3
                },
                'verbal': {
                    'keywords': ['verbal', 'language', 'communication', 'writing', 'reading', 'comprehension', 'linguistic'],
                    'weight': 2
                },
                'motivation': {
                    'keywords': ['motivation', 'drive', 'ambition', 'goals', 'aspiration', 'initiative'],
                    'weight': 2
                },
                'situational': {
                    'keywords': ['situation', 'scenario', 'judgment', 'decision-making', 'problem-solving', 'critical thinking'],
                    'weight': 3
                },
                'leadership': {
                    'keywords': ['leadership', 'management', 'supervision', 'team', 'coordination', 'direction'],
                    'weight': 2
                },
                'technical': {
                    'keywords': ['technical', 'skills', 'expertise', 'knowledge', 'proficiency', 'competence'],
                    'weight': 3
                }
            }
            
            # Score assessments based on multiple factors
            scored_assessments = []
            for assessment in self.db.assessments:
                score = 0
                
                # 1. Test type match (highest weight)
                for category, data in keyword_categories.items():
                    if category.lower() in assessment.test_type.lower():
                        score += data['weight'] * 2
                
                # 2. Description match
                for category, data in keyword_categories.items():
                    for keyword in data['keywords']:
                        if keyword in assessment.description.lower():
                            score += data['weight']
                
                # 3. Query match (highest weight for exact matches)
                for category, data in keyword_categories.items():
                    for keyword in data['keywords']:
                        if keyword in query:
                            score += data['weight'] * 2
                
                # 4. Duration consideration (shorter tests get a slight boost)
                if "minutes" in assessment.duration:
                    try:
                        duration = int(assessment.duration.split()[0])
                        if duration <= 30:
                            score += 1  # Boost for shorter tests
                    except:
                        pass
                
                # 5. Remote testing bonus
                if assessment.remote_testing:
                    score += 1
                
                # 6. Adaptive IRT bonus
                if assessment.adaptive_irt:
                    score += 1
                
                scored_assessments.append((score, assessment))
            
            # Sort by score and return top recommendations
            recommendations = [
                assessment for score, assessment in 
                sorted(scored_assessments, key=lambda x: x[0], reverse=True)
                if score > 0
            ][:max_results]
            
            if not recommendations:
                # If no matches found, return a mix of different types
                recommendations = []
                categories = list(keyword_categories.keys())
                for category in categories:
                    matching = [a for a in self.db.assessments if category.lower() in a.test_type.lower()]
                    if matching:
                        recommendations.append(matching[0])
                    if len(recommendations) >= max_results:
                        break
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in get_recommendations: {str(e)}")
            logger.error(traceback.format_exc())
            raise 