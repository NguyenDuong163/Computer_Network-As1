import mmap
import os

class FileSplitter:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def split_file_to_chunks(self, file_path: str, rng: tuple) -> list:
        try:
            # Open the file in read-write binary mode
            with open(file_path, "r+b") as f:
                # Create a memory-mapped view from the specified range
                mm = mmap.mmap(f.fileno(), 0)[rng[0]: rng[1]]
                # Divide each chunk into fixed-size pieces
                return [mm[p: p + self.chunk_size] for p in range(0, rng[1] - rng[0], self.chunk_size)]
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []

    def reassemble_file(self, chunks: list, output_path: str):
        try:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Open the output file in write binary mode
            with open(output_path, "bw+") as f:
                # Write each chunk to the output file
                for ch in chunks:
                    f.write(ch)
                f.flush()
                print(f"File reassembled and saved as {output_path}")
        except Exception as e:
            print(f"Error reassembling file: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "Design_Specification_Template.docx"
    output_directory = "output_chunks"
    chunk_size = 1024  # Specify the desired chunk size (in bytes)

    # Maximum size to be split 1m B
    start_byte = 0
    end_byte = 1000000 * 1024        

    splitter = FileSplitter(chunk_size)
    chunks = splitter.split_file_to_chunks(input_file, (start_byte, end_byte))

    # Reassemble the chunks into a new file
    output_file = os.path.join(output_directory, "word_reassembled.docx")
    splitter.reassemble_file(chunks, output_file)
