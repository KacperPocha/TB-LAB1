import hashlib
import json
from time import time


class Blockchain:

  def __init__(self):
    self.chain = []
    self.create_genesis_block()

  def create_genesis_block(self):
    genesis = {
        "index": 1,
        "timestamp": 0,
        "transactions": [],
        "nonce": 0,
        "previous_hash": "0" * 64,
    }
    self.chain.append(genesis)

  @staticmethod
  def hash(block):
    # sort_keys=True gwarantuje deterministyczną kolejność pól w JSON
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

  @property
  def last_block(self):
    return self.chain[-1]

  def add_block(self, transactions):
    block = {
        "index": len(self.chain) + 1,
        "timestamp": time(),
        "transactions": transactions,
        "nonce": 0,
        "previous_hash": self.hash(self.last_block),
    }
    self.chain.append(block)
    return block

  def is_chain_valid(self):
    for i in range(1, len(self.chain)):
      current_block = self.chain[i]
      previous_block = self.chain[i - 1]
      if current_block["previous_hash"] != self.hash(previous_block):
        return False, current_block["index"]

    return True, None

if __name__ == "__main__":
  bc = Blockchain()

  bc.add_block(["Alice -> Bob: 50 PLN"])
  bc.add_block(["Bob -> Carol: 2 PLN"])
  bc.add_block(["Janusz -> Andrzej: 13 PLN"])

  print("POCZĄTKOWY ŁAŃCUCH BLOKÓW")
  for block in bc.chain:
    print(json.dumps(block, indent=2, ensure_ascii=False))
    print("hash:", Blockchain.hash(block))

  valid, invalid_index = bc.is_chain_valid()
  print(f"Czy łańcuch jest poprawny?: {valid} (Niepoprawny blok: {invalid_index})\n")

  print("TEST 1: Sfałszowanie transakcji w bloku nr 2")
  bc.chain[1]["transactions"] = ["Alice -> Bob: 500"]

  valid, invalid_index = bc.is_chain_valid()
  print(f"Czy łańcuch jest poprawny po ataku?: {valid}")
  print(f"Wykryto błąd w bloku o indeksie: {invalid_index}\n")

  print(
      "TEST 2: Przeliczenie i nadpisanie previous_hash we wszystkich kolejnych"
      " blokach"
  )
  for i in range(1, len(bc.chain)):
    bc.chain[i]["previous_hash"] = bc.hash(bc.chain[i - 1])

  valid, invalid_index = bc.is_chain_valid()
  print(
      "Czy łańcuch jest poprawny po przeliczeniu hashów?:"
      f" {valid} (Niepoprawny blok: {invalid_index})"
  )


  print("TEST 3: Modyfikacja danych w ostatnim bloku")
  bc.chain[3]["transactions"] = ["Janusz -> Andrzej: 1000"]
  valid, invalid_index = bc.is_chain_valid()
  print(
      "Czy weryfikacja is_chain_valid() wykryła modyfikację ostatniego bloku?:"
      f" {valid}\n"
  )

  print("=" * 60)
  print("EKSPERYMENT: USUNIĘCIE sort_keys=True I ZMIANA KOLEJNOŚCI PÓŁ")


  def hash_without_sort(block):
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()

  # Blok A z standardową kolejnością pól
  block_a = {
      "index": 1,
      "timestamp": 0,
      "transactions": ["Alice -> Bob: 50"],
      "nonce": 0,
      "previous_hash": "0" * 64,
  }

  # Blok B z tą samą zawartością, ale ZMIENIONĄ kolejnością pól
  block_b = {
      "previous_hash": "0" * 64,
      "nonce": 0,
      "transactions": ["Alice -> Bob: 50"],
      "timestamp": 0,
      "index": 1,
  }

  print("1. Wyniki Z `sort_keys=True` (domyślna metoda w klasie):")
  print("   Hash Bloku A:", Blockchain.hash(block_a))
  print("   Hash Bloku B:", Blockchain.hash(block_b))

  print("\n2. Wyniki BEZ `sort_keys=True` (brak sortowania kluczy):")
  print("   Hash Bloku A:", hash_without_sort(block_a))
  print("   Hash Bloku B:", hash_without_sort(block_b))