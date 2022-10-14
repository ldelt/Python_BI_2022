def read_lenght(read):
    l_read = len(read)
    return l_read

def gc_content(read, r_lenght):
    counter_gc = 0
    for nuc in read:
        if nuc == 'G' or nuc == 'C':
            counter_gc = counter_gc + 1
    gc = (counter_gc / r_lenght) * 100
    return gc

def quality(line_q, r_lenght):
    q_score = []
    for q in line_q:
        q_score.append(ord(q) - 33)
    mean_q = sum(q_score) / r_lenght
    return mean_q

def passed(current_read, output_file_prefix):
	f_name = f'{output_file_prefix}_passed.fastq'
	with open(f_name, 'a') as passed_file:
		for line in current_read:
			passed_file.write(line)

def failed(current_read, output_file_prefix, save_filtered):
	if save_filtered == True:
		f_name = f'{output_file_prefix}_failed.fastq'
		with open(f_name, 'a') as failed_file:
			for line in current_read:
				failed_file.write(line)

def main(input_fastq, output_file_prefix, 
	gc_bounds = (0, 100), length_bounds = (0, 2**32), 
	quality_threshold = 0, save_filtered = False):

	with open(input_fastq, 'r') as file:
		counter_line = 0
		current_read = []

		for line in file:
			counter_line = counter_line + 1
			if (counter_line - 2) % 4 == 0:
				read = line.strip()
				r_lenght = read_lenght(read)
				gc = gc_content(read, r_lenght)

			if (counter_line - 4) % 4 == 0:
				line_q = line.strip()
				mean_q = quality(line_q, r_lenght)

			if len(current_read) == 4:
				if (((type(gc_bounds) is list) or (type(gc_bounds) is tuple)) and (gc < gc_bounds[0] or gc > gc_bounds[1])) or ((type(gc_bounds) is int) and gc >= gc_bounds):
					failed(current_read, output_file_prefix, save_filtered)
				elif (((type(length_bounds) is list) or (type(length_bounds) is tuple)) and (r_lenght < length_bounds[0] or r_lenght > length_bounds[1])) or ((type(length_bounds) is int) and r_lenght >= length_bounds):
					failed(current_read, output_file_prefix, save_filtered)
				elif mean_q < quality_threshold:
					failed(current_read, output_file_prefix, save_filtered)
				else:
					passed(current_read, output_file_prefix)
				current_read = []

			current_read.append(line)






