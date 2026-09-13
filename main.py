from src.image_processor import ImageProcessor


if __name__ == "__main__":
    processor = ImageProcessor()

    processor.process_batch_concurrent(
        input_dir="data/raw_images",
        output_dir="data/processed_images"
    )