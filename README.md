M3FEND 四个主要实验的单独运行指令
==========================================

这4个命令分别对应 --mode m3fend 会运行的4个实验配置

==========================================
实验1: 中文数据集 - 3个领域
==========================================
cd M3FEND-main
python run_experiments.py --mode single --dataset ch --domain_num 3 --model m3fend

或者直接使用 main.py:
python main.py --gpu 0 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 3

领域类别: 政治、医药健康、文体娱乐


==========================================
实验2: 中文数据集 - 6个领域
==========================================
cd M3FEND-main
python run_experiments.py --mode single --dataset ch --domain_num 6 --model m3fend

或者直接使用 main.py:
python main.py --gpu 0 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 6

领域类别: 教育考试、灾难事故、医药健康、财经商业、文体娱乐、社会生活


==========================================
实验3: 中文数据集 - 9个领域
==========================================
cd M3FEND-main
python run_experiments.py --mode single --dataset ch --domain_num 9 --model m3fend

或者直接使用 main.py:
python main.py --gpu 0 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 9

领域类别: 科技、军事、教育考试、灾难事故、政治、医药健康、财经商业、文体娱乐、社会生活


==========================================
实验4: 英文数据集 - 3个领域
==========================================
cd M3FEND-main
python run_experiments.py --mode single --dataset en --domain_num 3 --model m3fend

或者直接使用 main.py:
python main.py --gpu 0 --lr 0.0001 --model_name m3fend --dataset en --domain_num 3

领域类别: gossipcop、politifact、COVID


==========================================
使用说明
==========================================

1. 每个实验都是独立的，可以单独运行
2. 每个实验大约需要 1-2 小时（取决于硬件）
3. 结果会保存在: logs/json/m3fend.json
4. 如果使用 main.py，结果也会保存在同一个文件中

推荐使用方式:
- 如果想一次性运行所有4个: 使用 --mode m3fend
- 如果只想运行某个特定配置: 使用上面的单独命令
  
# Memory-Guided Multi-View Multi-Domain Fake News Detection (M<sup>3</sup>FEND)
This is the official implementation of our paper **Memory-Guided Multi-View Multi-Domain Fake News Detection**, which has been published in TKDE. [Paper](https://ieeexplore.ieee.org/document/9802916)

The wide spread of fake news is increasingly threatening both individuals and society. Great efforts have been made for automatic fake news detection on a single domain (e.g., politics). However, correlations exist commonly across multiple news domains, and thus it is promising to simultaneously detect fake news of multiple domains. Based on our analysis, we pose two challenges in multi-domain fake news detection: 1) **domain shift**, caused by the discrepancy among domains in terms of words, emotions, styles, etc. 2) **domain labeling incompleteness**, stemming from the real-world categorization that only outputs one single domain label, regardless of topic diversity of a news piece. In this paper, we propose a Memory-guided Multi-view Multi-domain Fake News Detection Framework (M<sup>3</sup>FEND) to address these two challenges. We model news pieces from a multi-view perspective, including semantics, emotion, and style. Specifically, we propose a Domain Memory Bank to enrich domain information which could discover potential domain labels based on seen news pieces and model domain characteristics. Then, with enriched domain information as input, a Domain Adapter could adaptively aggregate discriminative information from multiple views for news in various domains. Extensive offline experiments on English and Chinese datasets demonstrate the effectiveness of M<sup>3</sup>FEND, and online tests verify its superiority in practice.

## Introduction
This repository provides the implementations of M<sup>3</sup>FEND and ten baseline models (BiGRU, TextCNN, RoBERTa, StyleLSTM, DualEmotion, EANN, EDDFN, MMoE, MoSE, MDFEND). Note that TextCNN and BiGRU are implemented with word2vec as word embedding in the original experiments, but we implement them with RoBERTa embedding in this repository.

## Requirements

- Python 3.6
- PyTorch > 1.0
- Pandas
- Numpy
- Tqdm


## Run

Parameter Configuration:

- dataset: the English or Chinese dataset, default for `ch`
- early_stop: default for `3`
- domain_num: the Chinese dataset could choose 3, 6, and 9, while the English dataset could choose 3, default for `3`
- epoch: training epoches, default for `50`
- gpu: the index of gpu you will use, default for `0`
- lr: learning_rate, default for `0.0001`
- model_name: model_name within `textcnn bigru bert eann eddfn mmoe mose dualemotion stylelstm mdfend m3fend`, default for `m3fend`

You can run this code through:

```powershell
python main.py --gpu 1 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 3
```

```powershell
python main.py --gpu 1 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 6
```

```powershell
python main.py --gpu 1 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 9
```

```powershell
python main.py --gpu 1 --lr 0.0001 --model_name m3fend --dataset en --domain_num 3
```

The best learning rate for various models are different: BiGRU (0.0009), TextCNN (0.0007), RoBERTa (7e-05), StyleLSTM(0.0007), DualEmotion(0.0009), EANN (0.0001), EDDFN (0.0007), MDFEND (7e-5), M$^3$FEND (0.0001).


## Reference

```
Zhu, Yongchun, et al. "Memory-Guided Multi-View Multi-Domain Fake News Detection." IEEE Transactions on Knowledge and Data Engineering (2022).
```


```
Nan, Qiong, et al. "MDFEND: Multi-domain fake news detection." Proceedings of the 30th ACM International Conference on Information & Knowledge Management. 2021.
```

or in bibtex style:

```
@article{zhu2022memory,
  title={Memory-Guided Multi-View Multi-Domain Fake News Detection},
  author={Zhu, Yongchun and Sheng, Qiang and Cao, Juan and Nan, Qiong and Shu, Kai and Wu, Minghui and Wang, Jindong and Zhuang, Fuzhen},
  journal={IEEE Transactions on Knowledge and Data Engineering},
  year={2022},
  publisher={IEEE}
}
@inproceedings{nan2021mdfend,
  title={MDFEND: Multi-domain fake news detection},
  author={Nan, Qiong and Cao, Juan and Zhu, Yongchun and Wang, Yanyan and Li, Jintao},
  booktitle={Proceedings of the 30th ACM International Conference on Information \& Knowledge Management},
  pages={3343--3347},
  year={2021}
}
```
