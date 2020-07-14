from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from utils.vocab import Vocab
import torch

class ParallelDataset(Dataset):

	def __init__(self, source_name, target_name, max_length=300, source_vocab=None, target_vocab=None):

		self.data_source = self.read_file(source_name)
		self.data_target = self.read_file(target_name)

		self.max_length = max_length

		self.source_vocab = source_vocab
		if source_vocab == None:
			self.source_vocab = Vocab()
			self.source_vocab.build_vocab([source_name])

		self.target_vocab = target_vocab
		if target_vocab == None:
			self.target_vocab = Vocab()
			self.target_vocab.build_vocab([target_name])

			
	def __len__(self):
		return len(self.data_source)

	def __getitem__(self, index):

		print(self.data_source[index])
		src_tokens = self.padding_sentences(self.data_source[index])
		tgt_tokens = self.padding_sentences(self.data_target[index])

		src_tokens_ids = self.source_vocab.convert_sentence_to_ids(src_tokens)
		src_tokens_ids_tensor = torch.tensor(src_tokens_ids)

		tgt_tokens_ids = self.target_vocab.convert_sentence_to_ids(tgt_tokens)
		tgt_tokens_ids_tensor = torch.tensor(tgt_tokens_ids)


		return src_tokens_ids_tensor, tgt_tokens_ids_tensor


	def read_file(self, filename):
		data = []
		with open(filename, "r") as f:
			for line in f:
				data.append(line.strip().split()) 
		return data

	def padding_sentences(self, sentences):
		tokens = []
		for sentence in sentences:
			tokens.append(self.padding_sentence(sentence))
		return tokens


	def padding_sentence(self, tokens):
		tokens = ['<sos>'] + list(tokens) + ['<eos>']

		if len(tokens) < self.max_length:
			tokens = tokens + ['<pad>' for _ in range(self.max_length - len(tokens))]
		else:
			tokens = tokens[:self.max_length-1] + ['<eos>']

		return tokens


	def vocabs(self):
		return self.source_vocab, self.target_vocab


def get_dataloader (dataset, batch_size, shuffle=False):
	return DataLoader(dataset, batch_size = batch_size, shuffle = shuffle, num_workers = 5)



