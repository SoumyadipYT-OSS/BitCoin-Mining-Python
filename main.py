import time
import logging
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor

# Constants
MAX_NONCE = 100000000000
NUM_THREADS = 4     # This is for parallel mining using 4 threads

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def sha256_hash(txt):
    return sha256(txt.encode("ascii")).hexdigest()


def mine_block(blockNum, transactions, previous_hash, prefix_zeros, start_nonce, end_nonce):
    prefix_string = '0' * prefix_zeros
    for i_nonce in range(start_nonce, end_nonce):
        generateText = f"{blockNum}{transactions}{previous_hash}{i_nonce}"
        new_hash = sha256_hash(generateText)
        if new_hash.startswith(prefix_string):
            logging.info(f"Successfully mined bitcoins with nonce value: {i_nonce}")
            return new_hash, i_nonce
    return None, None


# Uses multiple threads to mine a block.
def parallel_mine(block_number, transactions, previous_hash, prefix_zeros):
    chunk_size = MAX_NONCE // NUM_THREADS
    futures = []
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for i in range(NUM_THREADS):
            start_nonce = i * chunk_size
            end_nonce = start_nonce + chunk_size
            futures.append(executor.submit(mine_block, block_number, transactions, previous_hash, prefix_zeros, start_nonce, end_nonce))
        
        for future in futures:
            result, nonce = future.result()
            if result:
                return result, nonce
            
    raise Exception(f"Couldn't find correct hash after trying {MAX_NONCE} times")


if __name__=="__main__":
    transactions = """
    Player1 -> Player2 -> 200,
    Player3 -> Player4 -> 450
    """
    difficulty = 6      # Increase this number to make mining more difficult

    start_time = time.time()
    logging.info("Start mining...")

    try:
        new_hash, nonce = parallel_mine(
            block_number=5,
            transactions=transactions,
            previous_hash="0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7",
            prefix_zeros=difficulty
        )
        end_time = time.time()
        total_time = end_time - start_time

        logging.info(f"End mining. Mining took: {total_time:.2f} seconds")
        logging.info(f"New hash: {new_hash}")
        logging.info(f"Nonce: {nonce}")
    except Exception as e:
        logging.error(e)
