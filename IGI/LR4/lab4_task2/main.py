from text_analysis import *

def main():
    input_file = 'text_input.txt'
    output_file = 'output/analysis.txt'
    archive = 'output/archive.zip'

    # Step 1: Read text
    text = read_text(input_file)

    # Step 2: Analyze
    result = analyze_text(text)

    # Step 3: Save results
    save_results(output_file, result)
    print(f"Analysis saved to {output_file}")

    # Step 4: Archive
    archive_file(output_file, archive)
    print(f"Archived to {archive}")

    # Step 5: Show archive info
    print(archive_info(archive))

if __name__ == "__main__":
    main()