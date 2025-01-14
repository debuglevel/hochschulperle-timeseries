import os
import glob
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime

# Directory containing the XML files
directory = '.'

# Dictionary to store the data
data = {}

print("Reading XML files from directory:", directory)
# Read and parse XML files
for file in glob.glob(os.path.join(directory, '2025-*')):
    print("Reading file:", file)
    tree = ET.parse(file)
    root = tree.getroot()

    # Extract datetime from the filename
    filename = os.path.basename(file)
    print("Filename:", filename)
    file_datetime = datetime.strptime(filename, '%Y-%m-%d %H-%M')
    print("Datetime:", file_datetime)

    # Extract keywords and votes
    for keyword in root.findall('.//keyword'):
        print("Keyword:", keyword.find('name').text.strip())
        name = keyword.find('name').text.strip()
        votes = int(keyword.find('stimmen').text.strip())

        if name not in data:
            data[name] = []
        data[name].append((file_datetime, votes))

print(data)

# Plot the data
print("Plotting the data")
plt.figure(figsize=(10, 6))

for name, values in data.items():
    values.sort()  # Sort by datetime
    dates, votes = zip(*values)
    plt.plot(dates, votes, label=name)

plt.xlabel('Date and Time')
plt.ylabel('Votes')
plt.title('Time Series of Votes for Each Keyword')
plt.legend()
plt.grid(True)
#plt.show()

plt.savefig('plot.svg', format='svg')
