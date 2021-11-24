txdata = "0x202ee0ed00000000000000000000000000000000000000000000000000000000000064270000000000000000000000000000000000000000000000000000002b3b0ddcaa"


def count_zero_bytes(data):
  count = 0
  for i in range(0, len(data), 2):
    byte = data[i:i+2]
    if byte == "00":
      count += 1
  return count

def count_non_zero_bytes(data):
  return (len(data) / 2) - count_zero_bytes(data)

print("zero-bytes: {0}".format(count_zero_bytes(txdata)))
print("non-zero-bytes: {0}".format(count_non_zero_bytes(txdata)))

# OUTPUT
# zero-bytes: 184
# non-zero-bytes: 1594