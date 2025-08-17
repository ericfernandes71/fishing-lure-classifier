#!/usr/bin/env python3
"""
Training Pipeline for Fishing Lure Classifier
Uses ChatGPT Vision to generate training data and trains a custom CNN model
"""

import os
import json
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import seaborn as sns
from enhanced_hybrid_classifier import EnhancedHybridLureClassifier
import datetime

class LureTrainingPipeline:
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.hybrid_classifier = None
        self.label_encoder = LabelEncoder()
        self.model = None
        self.training_history = None
        
        if openai_api_key:
            self.hybrid_classifier = EnhancedHybridLureClassifier(openai_api_key)
    
    def generate_training_dataset(self, image_folder: str, output_file: str = None) -> dict:
        """
        Generate training dataset using ChatGPT Vision analysis
        """
        if not self.hybrid_classifier:
            raise ValueError("Hybrid classifier not initialized. Please provide OpenAI API key.")
        
        print("🚀 Starting training dataset generation...")
        print(f"📁 Scanning folder: {image_folder}")
        
        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        image_files = []
        
        for file in os.listdir(image_folder):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(image_folder, file))
        
        print(f"📸 Found {len(image_files)} images")
        
        if not image_files:
            raise ValueError("No images found in the specified folder")
        
        # Generate training data
        training_data = self.hybrid_classifier.generate_training_data(image_files)
        
        # Save to file
        if not output_file:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"training_dataset_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        print(f"💾 Training dataset saved to: {output_file}")
        print(f"📊 Dataset contains {training_data['total_samples']} samples")
        print(f"🏷️ Label distribution: {training_data['lure_type_distribution']}")
        
        return training_data
    
    def prepare_training_data(self, training_data: dict, image_folder: str, img_size: tuple = (224, 224)) -> tuple:
        """
        Prepare images and labels for training
        """
        print("🔧 Preparing training data...")
        
        X = []  # Images
        y = []  # Labels
        
        for sample in training_data['samples']:
            image_path = sample['image_path']
            label = sample['label']
            
            try:
                # Load and preprocess image
                image = cv2.imread(image_path)
                if image is not None:
                    # Resize image
                    image = cv2.resize(image, img_size)
                    # Convert BGR to RGB
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    # Normalize pixel values
                    image = image.astype(np.float32) / 255.0
                    
                    X.append(image)
                    y.append(label)
                else:
                    print(f"⚠️ Could not load image: {image_path}")
            except Exception as e:
                print(f"❌ Error processing {image_path}: {str(e)}")
        
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        
        print(f"✅ Prepared {len(X)} images with shape {X.shape}")
        print(f"🏷️ Labels: {np.unique(y)}")
        
        return X, y
    
    def create_model(self, num_classes: int, img_size: tuple = (224, 224)) -> tf.keras.Model:
        """
        Create a CNN model for lure classification
        """
        print("🏗️ Creating CNN model...")
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=(*img_size, 3)),
            
            # Convolutional layers
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and dense layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Model created successfully!")
        model.summary()
        
        return model
    
    def train_model(self, X: np.ndarray, y: np.ndarray, 
                   validation_split: float = 0.2,
                   epochs: int = 50,
                   batch_size: int = 32) -> dict:
        """
        Train the CNN model
        """
        print("🚀 Starting model training...")
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        num_classes = len(self.label_encoder.classes_)
        
        print(f"🏷️ Encoded labels: {self.label_encoder.classes_}")
        print(f"📊 Number of classes: {num_classes}")
        
        # Create model
        img_size = (X.shape[1], X.shape[2])
        self.model = self.create_model(num_classes, img_size)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y_encoded, test_size=validation_split, random_state=42, stratify=y_encoded
        )
        
        print(f"📚 Training samples: {len(X_train)}")
        print(f"🧪 Validation samples: {len(X_val)}")
        
        # Data augmentation
        data_augmentation = tf.keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomBrightness(0.2),
            layers.RandomContrast(0.2),
        ])
        
        # Add augmentation to training data
        X_train_augmented = data_augmentation(X_train)
        
        # Training callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', patience=10, restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7
            ),
            tf.keras.callbacks.ModelCheckpoint(
                'best_lure_model.h5', monitor='val_accuracy', save_best_only=True
            )
        ]
        
        # Train model
        self.training_history = self.model.fit(
            X_train_augmented,
            y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        print("✅ Training completed!")
        
        return {
            'model': self.model,
            'history': self.training_history,
            'label_encoder': self.label_encoder,
            'training_samples': len(X_train),
            'validation_samples': len(X_val)
        }
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """
        Evaluate the trained model
        """
        if self.model is None:
            raise ValueError("No trained model available")
        
        print("🔍 Evaluating model...")
        
        # Encode test labels
        y_test_encoded = self.label_encoder.transform(y_test)
        
        # Predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = np.argmax(y_pred_proba, axis=1)
        
        # Calculate metrics
        test_accuracy = np.mean(y_pred == y_test_encoded)
        
        # Confusion matrix
        from sklearn.metrics import confusion_matrix, classification_report
        
        cm = confusion_matrix(y_test_encoded, y_pred)
        
        # Classification report
        report = classification_report(
            y_test_encoded, y_pred, 
            target_names=self.label_encoder.classes_,
            output_dict=True
        )
        
        results = {
            'test_accuracy': test_accuracy,
            'confusion_matrix': cm,
            'classification_report': report,
            'predictions': y_pred,
            'true_labels': y_test_encoded,
            'prediction_probabilities': y_pred_proba
        }
        
        print(f"📊 Test Accuracy: {test_accuracy:.4f}")
        print(f"🏷️ Classes: {self.label_encoder.classes_}")
        
        return results
    
    def plot_training_history(self, save_path: str = None):
        """
        Plot training history
        """
        if self.training_history is None:
            print("❌ No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Accuracy plot
        ax1.plot(self.training_history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.training_history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(self.training_history.history['loss'], label='Training Loss')
        ax2.plot(self.training_history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Training history plot saved to: {save_path}")
        
        plt.show()
    
    def plot_confusion_matrix(self, confusion_matrix: np.ndarray, save_path: str = None):
        """
        Plot confusion matrix
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            confusion_matrix, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.label_encoder.classes_,
            yticklabels=self.label_encoder.classes_
        )
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Confusion matrix plot saved to: {save_path}")
        
        plt.show()
    
    def save_model(self, model_path: str = None):
        """
        Save the trained model and label encoder
        """
        if self.model is None:
            print("❌ No trained model available")
            return
        
        if not model_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = f"lure_classifier_model_{timestamp}"
        
        # Save model
        model_file = f"{model_path}.h5"
        self.model.save(model_file)
        
        # Save label encoder
        encoder_file = f"{model_path}_labels.json"
        with open(encoder_file, 'w') as f:
            json.dump({
                'classes': self.label_encoder.classes_.tolist(),
                'classes_': self.label_encoder.classes_.tolist()
            }, f, indent=2)
        
        print(f"💾 Model saved to: {model_file}")
        print(f"🏷️ Labels saved to: {encoder_file}")
        
        return model_file, encoder_file
    
    def predict_single_image(self, image_path: str) -> dict:
        """
        Predict lure type for a single image
        """
        if self.model is None:
            raise ValueError("No trained model available")
        
        # Load and preprocess image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Resize and preprocess
        image = cv2.resize(image, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        
        # Predict
        prediction_proba = self.model.predict(image)
        predicted_class_idx = np.argmax(prediction_proba[0])
        predicted_class = self.label_encoder.classes_[predicted_class_idx]
        confidence = prediction_proba[0][predicted_class_idx]
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'all_probabilities': {
                self.label_encoder.classes_[i]: float(prediction_proba[0][i])
                for i in range(len(self.label_encoder.classes_))
            }
        }

def main():
    """Example usage of the training pipeline"""
    print("🎣 Fishing Lure Training Pipeline")
    print("=" * 50)
    
    # Initialize pipeline (you'll need to add your OpenAI API key)
    pipeline = LureTrainingPipeline()
    
    print("💡 To use the full pipeline, initialize with your OpenAI API key:")
    print("   pipeline = LureTrainingPipeline(openai_api_key='your-key-here')")
    
    print("\n🚀 Available methods:")
    print("   1. generate_training_dataset(folder) - Generate training data with ChatGPT")
    print("   2. prepare_training_data(data, folder) - Prepare images for training")
    print("   3. create_model(num_classes) - Create CNN architecture")
    print("   4. train_model(X, y) - Train the model")
    print("   5. evaluate_model(X_test, y_test) - Evaluate performance")
    print("   6. save_model(path) - Save trained model")
    print("   7. predict_single_image(path) - Make predictions")
    
    print("\n📚 Complete workflow:")
    print("   1. Set up OpenAI API key")
    print("   2. Generate training dataset using ChatGPT Vision")
    print("   3. Prepare and preprocess images")
    print("   4. Train custom CNN model")
    print("   5. Evaluate and save model")
    print("   6. Use for predictions")

if __name__ == "__main__":
    main()
