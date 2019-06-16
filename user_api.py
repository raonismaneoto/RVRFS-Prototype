import util
import json

def create_file(args):
	file_name = args[0]
	check_file_oneness(file_name)
	inode = util.get_inode(sb.get_inode_number())
	inode.block_list.append(sb.get_block_number())
	inode.file_name = file_name
	util.create_empty_inode(sb.isize)
	util.create_empty_block(sb.bsize)
	root_inode.write({file_name: inode.number})
	util.save(inode.bytefy(), inode.get_offset(), 'disk')
	util.save(sb.bytefy(), 0, 'disk')
	print util.get_inode(inode.number).bytefy()

def read_file(args):
	file_name = args[0]
	inode_number = -1
	blist = root_inode.block_list
	inode = {}
	for block_number in blist:
		block = util.get_block(block_number)
		for file_descriptor in block.data:
			if type(file_descriptor) == dict and file_name in file_descriptor.keys():
				inode_number = file_descriptor[file_name]
				break
	if inode_number != -1:
		inode = util.get_inode(inode_number)
	print_data(inode)
	return inode

def print_data(inode):
	if inode == {}:
		print inode
		return
	data = ''
	for block in inode.block_list:
		block = util.get_block(block)
		data += json.dumps(block.data)
	print data

def write_file(args):
	file_name = args[0]
	data = args[1]
	inode = read_file([file_name])
	print inode.__dict__
	if inode == {}:
		raise Exception("The file %s does not exist" %file_name)

	inode.write(data)

def check_file_oneness(file_name):
	blist = root_inode.block_list
	for block_number in blist:
		block = util.get_block(block_number)
		for file_descriptor in block.data:
			if type(file_descriptor) == dict and file_name in file_descriptor.keys():
				raise Exception("The file with name %s already exists" %file_name)

menu_options = {
	'create': create_file,
	'read': read_file,
	'write': write_file
}

sb = util.get_sb()
root_inode = util.get_inode(1)

while True:
	user_input = raw_input().split(" ")
	operation = menu_options[user_input[0]]
	operation(user_input[1:])

