def fingerprint_image_match(image1_path, image2_path, threshold=0.9):
    from PIL import Image
    import imagehash

    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)

    # Calculate similarity between the two hashes
    similarity = 1.0 - (hash1 - hash2) / len(hash1.hash)  # Normalized Hamming distance

    # Compare the similarity with the threshold and return the result
    return similarity >= threshold

print(fingerprint_image_match('noyon.bmp','noyon2.bmp'))