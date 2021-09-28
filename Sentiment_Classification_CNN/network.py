import torch.nn as nnimport torch.optim as optimfrom pytorch_lightning import LightningModulefrom model import CNNClassifierfrom torchmetrics import Accuracyclass Classifier(LightningModule):    def __init__(self,                 model=None,                 n_words=None,                 lr=1e-4):        super(Classifier, self).__init__()        if model is None:            assert n_words is not None, 'vocab size를 정의해주세요'            self.model = CNNClassifier(n_words=n_words)        else:            self.model = model        self.lr = lr        self.loss_fn = nn.NLLLoss()        self.metrics = Accuracy()    def configure_optimizers(self):        return optim.AdamW(params=self.model.parameters(),                           lr=self.lr)    def forward(self, x):        return self.model(x)    def training_step(self, batch, batch_idx):        x, y = batch        y_hat = self.model(x)        loss = self.loss_fn(y_hat, y)        self.log('train_loss_step', loss, on_step=True, on_epoch=False, prog_bar=True)        self.log('train_loss_epoch', loss, on_step=False, on_epoch=True, prog_bar=False)    def validation_step(self, batch, batch_idx):        x, y = batch        y_hat = self.model(x)        loss = self.loss_fn(y_hat, y)        self.metrics(preds=y_hat,                     target=y)        self.log('val_loss', loss, on_step=True, on_epoch=True, prog_bar=False)        self.log('Accuracy', self.metrics, on_step=False, on_epoch=True, prog_bar=False)