# ACL_Sorter

## Table of Contents
- [About The Project](#about-the-project)
- [Built With](#built-with)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Future Plans](#future-plans)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#Acknowledgements)

## About the Project
This project processes a text file containing a switch's IP access list and generates the necessary configuration commands to remove outdated entries and reorganize the access list in ascending IP address order.

I created this project to address the common issue of disorganized access lists at work, which often leads to unnecessary delays when locating the correct IP to add or remove. This tool is designed to help streamline and reorganize client switch access lists, making future modifications more efficient and reducing time spent on manual edits.


## Built With
- [Python](https://www.python.org/)

### Prerequisites
   Before starting, make sure you have the following:
   - Python


## Usage
Instructions:
Paste the ACL you want to organize into the file named original_ACL.txt, then run the script sort_ACL.py. After execution, the generated configuration commands will be saved in new_organized_ACL.txt.

Important Note:
The output contains partial configuration commands intended to help organize your ACL. These commands are not a complete replacement for a full configuration and should not be pasted directly into your switch without proper the other configuration commands that are not provided by this project. Doing so may lead to errors or unintended behavior.


## How It Works
This project processes the ACL data found in original_ACL.txt. It begins by reading the file and converting each line into a list of strings, using the space (" ") character as the delimiter.

Example:

"10 permit igmp any host 239.1.1.1"  
→ ['10', 'permit', 'igmp', 'any', 'host', '239.1.1.1']

This step removes unnecessary indentation and allows for easier manipulation of each element—particularly the IP addresses.

Each line (now a list of its components) is stored inside a larger list, making it easy to pass data between functions for further processing.
Step 1: Preparing the Switch Configuration

Before sorting the IPs, the script writes each line to new_organized_ACL.txt with no prepended to each command.

Why?
This ensures that when you re-add the reorganized ACL, the existing rules are cleared first. This prevents duplicate entries and avoids errors on the switch.
Step 2: Parsing and Sorting the IPs

Next, the script isolates the IP addresses by splitting them by the period (".") character and converting each octet into an integer for accurate comparison.

Example:

['10', 'permit', 'igmp', 'any', 'host', '239.1.1.1']  
→ [239, 1, 1, 1]

This results in a list of lists, each representing an IP address in numerical form:

[[239, 1, 1, 1], [239, 1, 1, 4], [239, 1, 1, 2], [238, 1, 1, 2], [240, 1, 1, 2], [238, 1, 1, 1]]

Step 3: Recursive Sorting

To sort the IPs, the script uses a recursive strategy similar to quicksort:

    Select a "base" IP from the middle of the list.

    Compare each IP’s current octet to the base:

        Less than → goes into the Less Than list

        Equal to → goes into the Equal To list (and moves to the next octet)

        Greater than → goes into the More Than list

    Recursively repeat this process until each list contains only one IP.

Example:

1st Recursion — Compare 1st octet  
Base: [238, 1, 1, 2]  
Less: []  
Equal: [[238, 1, 1, 2], [238, 1, 1, 1]]  
More: [[239, 1, 1, 1], [239, 1, 1, 4], [239, 1, 1, 2], [240, 1, 1, 2]]

2nd Recursion — Compare 2nd octet in Equal list, etc.

This continues until all IPs are sorted in correct order:

[[238, 1, 1, 1], [238, 1, 1, 2], [239, 1, 1, 1], [239, 1, 1, 2], [239, 1, 1, 4], [240, 1, 1, 2]]

Current Limitation

Due to a known bug (planned to be fixed), the script currently returns the sorted IPs in a flat list:

[238, 1, 1, 1, 238, 1, 1, 2, 239, 1, 1, 1, 239, 1, 1, 2, 239, 1, 1, 4, 240, 1, 1, 2]

As a workaround, the script groups the values into sublists of four to recreate the intended structure.
Final Step: Writing to Output

Once sorted, the IPs are reintegrated into their original ACL commands with appropriate prefixes and written to new_organized_ACL.txt as the final output.


## Future Plans
[ ] Quick IP Check
- After discussing with a coworker, she confirmed that having a faster method to check whether a list of IPs exists in the access list would also significantly improve efficiency. I'd like to add this feature to the project, even though it wasn't part of the original goal, as it further enhances efficiency in our daily workflow.


## Conributing
   Thank you for your interest! However, I am currently not accepting external contributions to this project.


## License
   To be determined. This project is currently not licensed for reuse.


## Contact
Sean Susmerano - - susmeranosean@gmail.com
Project Link: https://github.com/SeanSusmerano/MTG-Card-Lookup
