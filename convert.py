import argparse
import os
import subprocess
import zipfile

parser = argparse.ArgumentParser(
    prog="convert.py",
    description="converts lecture notes in adoc format into either HTML or PDF",
    epilog="my name jeff",
)

parser.add_argument("-dirpath", "-d")
parser.add_argument("-outname", "-o")
parser.add_argument("-filetype", "-t")

args = parser.parse_args()

dirpath, outname, filetype = (args.dirpath, args.outname, args.filetype)


# Get current working directory
target = dirpath

# Filter for lecture directories
lectures = filter(lambda d: d.startswith("lec"), os.listdir(target))

for lecture in lectures:
    # Create full path to lecture directory
    lecture_path = os.path.join(target, lecture)

    # Filter for .adoc files in the lecture directory
    adocs = filter(lambda f: f.endswith(".adoc"), os.listdir(lecture_path))

    for adoc in adocs:
        # Create full path to .adoc file
        adoc_path = os.path.join(lecture_path, adoc)

        match filetype:
            case "html":
                subprocess.run(["asciidoctor-pdf", adoc_path])
            case "pdf":
                subprocess.run(["asciidoctor-pdf", adoc_path])
            case _:
                raise ValueError(
                    f"filetype must be one of html, pdf but found {filetype}"
                )

zip_filename = f"{outname}.zip"
# Now, create a ZIP file with all converted files
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(target):
        for file in files:
            if file.endswith(f".{filetype}"):
                # Get the full path to the converted file
                file_path = os.path.join(root, file)

                # Create a relative path for the file in the ZIP
                # This preserves the directory structure within the ZIP
                rel_path = os.path.relpath(file_path, start=target)

                # Add the file to the ZIP
                zipf.write(file_path, rel_path)
