import random

def generate_random_numbers(seed_value):
  # Convert the seed value to an integer using its hash
  seed = int(hash(seed_value))

  # Set the seed
  random.seed(seed)

  # Generate 4 random numbers
  random_numbers = set()
  while len(random_numbers) < 4:
    random_numbers.add(random.randint(1, 6))

  return list(random_numbers)

  # random_numbers = [random.randint(1,8)  for _ in range(4)]

  # return random_numbers