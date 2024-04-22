import os

def file_split(file_path: str, chunk_size: int):
    def split_file_to_chunks(file_path: str, chunk_size: int):
        try:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break  # Đã đọc hết tệp
                    yield chunk
        except FileNotFoundError:
            print(f"Can not find: {file_path}")

    def save_chunks_to_directory(chunks: list, output_directory: str, file_name: str, file_exten: str):
        try:
            os.makedirs(output_directory, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
            for i, chunk in enumerate(chunks):
                output_file = os.path.join(output_directory, f"{file_name}_{file_exten}_{i}.bin")
                with open(output_file, "wb") as out_f:
                    out_f.write(chunk)
                print(f"Chunk created {i}: {output_file}")
        except Exception as e:
            print(f"Chunks saving error {e}")

    # Get the file name without extension
    file_name, file_exten = os.path.splitext(os.path.basename(file_path)) #Take input file's name and extension
    file_name = file_name.replace('.', '_')  # Replace '.' in file name with '_'
    file_exten = file_exten.replace('.', '')  # Remove '.' from file extension

    chunks = list(split_file_to_chunks(file_path, chunk_size))
    save_chunks_to_directory(chunks, f"{file_name}_{file_exten}", file_name, file_exten)

    return len(chunks)  # Return the number of chunks

# Ví dụ sử dụng
if __name__ == "__main__":
    input_file = "input136.txt"  # Full path to the file, plz use '\\' instead of '\' :( this language is shite
    chunk_size =  50 * 1024  # Kích thước chunk mong muốn (tùy chỉnh)

    num_chunks = file_split(input_file, chunk_size)
    print(f"Number of chunks created: {num_chunks}")
