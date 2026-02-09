# 快速启动指南

## 已完成的设置

1. ✅ 已创建 `requirements.txt` 文件，包含所有必要的依赖
2. ✅ 已解压数据文件（`data/ch/` 和 `data/en/` 目录下的 pkl 文件）
3. ✅ 已安装所有依赖包
4. ✅ 已修复代码中的目录创建问题
5. ✅ 已优化代码以支持 CPU 模式（自动检测 CUDA 是否可用）

## 运行代码

### 基本运行命令

使用中文数据集（默认）：
```powershell
python main.py --gpu 0 --lr 0.0001 --model_name m3fend --dataset ch --domain_num 3
```

使用英文数据集：
```powershell
python main.py --gpu 0 --lr 0.0001 --model_name m3fend --dataset en --domain_num 3
```

### 参数说明

- `--model_name`: 模型名称，可选值：`textcnn`, `bigru`, `bert`, `eann`, `eddfn`, `mmoe`, `mose`, `dualemotion`, `stylelstm`, `mdfend`, `m3fend`（默认：`m3fend`）
- `--dataset`: 数据集，`ch`（中文）或 `en`（英文），默认：`ch`
- `--domain_num`: 领域数量，中文数据集可选 3、6、9，英文数据集只能选 3，默认：`3`
- `--gpu`: GPU 索引，如果没有 GPU 或使用 CPU，设置为 `0`（代码会自动检测）
- `--lr`: 学习率，默认：`0.0001`
- `--epoch`: 训练轮数，默认：`50`
- `--batchsize`: 批次大小，默认：`64`

### 注意事项

1. **GPU/CPU 模式**：代码会自动检测 CUDA 是否可用。如果没有 GPU，代码会在 CPU 模式下运行（速度较慢）。

2. **首次运行**：首次运行时会自动下载预训练模型：
   - 中文数据集：`hfl/chinese-bert-wwm-ext`
   - 英文数据集：`roberta-base`
   这可能需要一些时间和网络连接。

3. **输出目录**：
   - 日志文件：`./logs/`
   - 模型参数：`./param_model/`
   - JSON 结果：`./logs/json/`

4. **推荐的学习率**（根据 README）：
   - BiGRU: 0.0009
   - TextCNN: 0.0007
   - RoBERTa (bert): 7e-05
   - StyleLSTM: 0.0007
   - DualEmotion: 0.0009
   - EANN: 0.0001
   - EDDFN: 0.0007
   - MDFEND: 7e-5
   - M³FEND: 0.0001

## 依赖包

所有依赖已安装在 `requirements.txt` 中：
- torch>=1.0.0
- transformers>=4.0.0
- pandas>=1.0.0
- numpy>=1.19.0
- tqdm>=4.50.0
- scikit-learn>=0.23.0

## 故障排除

如果遇到问题：

1. **导入错误**：确保所有依赖都已安装：
   ```powershell
   pip install -r requirements.txt
   ```

2. **数据文件错误**：确保 `data/ch/` 和 `data/en/` 目录下都有 `train.pkl`, `val.pkl`, `test.pkl` 文件

3. **CUDA 错误**：如果没有 GPU，代码会自动使用 CPU，但训练速度会很慢

4. **内存不足**：可以尝试减小 `--batchsize` 参数（例如：`--batchsize 32`）
