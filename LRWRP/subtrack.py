import subprocess

def extract_subtitle(mkv_file_path, output_txt_file_path):
    """
    Extracts the first subtitle track from an MKV file and saves it as a TXT file.

    :param mkv_file_path: Path to the MKV video file.
    :param output_txt_file_path: Path where the extracted subtitle should be saved as a TXT file.
    """
    try:
        # Running the FFmpeg command to extract subtitles
        command = ["ffmpeg", "-i", mkv_file_path, "-map", "0:s:0", "-scodec", "srt", "-f", "rawvideo", output_txt_file_path]
        subprocess.run(command, check=True)
        return "Subtitle extracted successfully."
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

# Example usage
# extract_subtitle("example.mkv", "output.txt")
