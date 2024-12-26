import pickle

with open("wordList.dat","wb") as file:
    words = [
    "Stapler", "Desk", "Pay cheque", "Work computer", "Phone", "Paper", "Light", "Chair", "Desk lamp",
    "Notepad", "Paper clips", "Binder", "Calendar", "Sticky Notes", "Pens", "Pencils", "Notebook",
    "Book", "Chairs", "Coffee mug", "Thermos", "Hot cup", "Glue", "Clipboard", "Paperclips",
    "Secretary", "Work", "Paperwork", "Workload", "Employee", "Boredom", "Coffee", "Laptop",
    "Sandcastle", "Monday", "Vanilla", "Bamboo", "Sneeze", "Scratch", "Celery", "Hammer", "Frog", "Tennis",
    "Hot dog", "Pants", "Bridge", "Bubblegum", "Candy bar", "Bucket", "Skiing", "Sledding", "Snowboarding",
    "Snowman", "Polar bear", "Cream", "Waffle", "Pancakes", "Ice cream", "Sundae", "Beach", "Sunglasses",
    "Surfboard", "Watermelon", "Baseball", "Bat", "Ball", "T-shirt", "Kiss", "Jellyfish", "Jelly", "Butterfly",
    "Spider", "Broom", "Spiderweb", "Mummy", "Candy", "Bays", "Squirrels", "Basketball", "Water Bottle", "Unicorn",
    "Dog leash", "Newspaper", "Hammock", "Video camera", "Money", "Smiley face", "Umbrella", "Picnic basket",
    "Teddy bear", "Ambulance", "Ancient Pyramids", "Bacteria", "Goosebumps", "Pizza", "Platypus", "Clam Chowder",
    "Goldfish bowl", "Skull", "Spiderweb", "Smoke", "Tree", "Ice", "Blanket", "Seaweed", "Flame", "Bubble", "Hair",
    "Tooth", "Leaf", "Worm", "Sky", "Apple", "Plane", "Cow", "House", "Dog", "Car", "Bed", "Furniture"
]
    
    pickle.dump(words,file)
