"""
SmartResume AI — Model Training and Evaluation Pipeline Runner

Trains KNN, Logistic Regression, SVM, Decision Tree, and Naive Bayes,
displays evaluation metrics, and saves the champion model.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.ml_recommender import MLRecommender

def main():
    print("=" * 80)
    print("  SmartResume AI — Machine Learning Model Training & Evaluation Suite")
    print("=" * 80)
    
    recommender = MLRecommender()
    metrics = recommender.train_and_compare_models()
    
    print("\n[+] Dataset & Feature Summary:")
    print(f"    - Total Generated Samples: {metrics['total_samples']}")
    print(f"    - Training Set (80%):      {metrics['train_samples']} samples")
    print(f"    - Test Set (20%):          {metrics['test_samples']} samples")
    print(f"    - Number of Target Roles:  {metrics['num_classes']} classes")
    print(f"    - TF-IDF Feature Dimension:{metrics['feature_count']} features")
    
    print(f"\n[+] Champion Model: {metrics['champion_model']}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
