import torch.nn as nnfrom TorchCRF import CRFfrom transformers import BertModelclass BertCRFNER(nn.Module):    def __init__(self,                 pretrained_model_name: str = "kykim/bert-kor-base",                 freeze: bool = True,                 num_tags: int = 14):        super(BertNER, self).__init__()        self.bert_model = BertModel.from_pretrained(pretrained_model_name)        if freeze:            for param in self.bert_model.parameters():                param.requires_grad = False        self.fc = nn.Linear(768, num_tags)        self.crf = CRF(num_tags=num_tags)    def forward(self, data, tags=None):        input_ids, token_type_ids, attention_mask = data.input_ids, data.token_type_ids, data.attention_mask        last_hidden_state = self.bert_model(input_ids=input_ids,                                            token_type_ids=token_type_ids,                                            attention_mask=attention_mask)['last_hidden_state']        bert_output = self.logit(last_hidden_state)        if tags is None:            return torch.Tensor(self.crf.decode(bert_output)).transpose(0, 1)        elif tags is not None:            loss, sequence_of_tags = -1 * self.crf(bert_output, tags), \                                     torch.Tensor(self.crf.decode(bert_output)).transpose(0, 1)            return loss, sequence_of_tags