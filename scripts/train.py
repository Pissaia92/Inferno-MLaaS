import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def create_mock_dataset():
    """Create a mock dataset for sentiment classification."""
    texts = [
        "I love this product",
        "Amazing quality and fast delivery",
        "Great service and friendly staff",
        "Outstanding experience",
        "Highly recommend this",
        "Terrible service",
        "Worst product ever",
        "Poor quality and slow shipping",
        "Very disappointed",
        "Awful experience",
        "Not worth the money",
        "Excellent customer support",
        "Perfect condition",
        "Fast shipping and good price",
        "Will buy again"
    ]
    
    labels = [
        1,  # positive
        1,  # positive
        1,  # positive
        1,  # positive
        1,  # positive
        0,  # negative
        0,  # negative
        0,  # negative
        0,  # negative
        0,  # negative
        0,  # negative
        1,  # positive
        1,  # positive
        1,  # positive
        1   # positive
    ]
    
    return texts, labels


def train_model():
    # Create pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    
    # Load mock dataset
    texts, labels = create_mock_dataset()
    
    # Train the model
    pipeline.fit(texts, labels)
    
    # Save the trained model
    joblib.dump(pipeline, 'model.pkl')
    print("Model trained and saved as model.pkl")


if __name__ == "__main__":
    train_model()