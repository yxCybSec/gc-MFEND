"""
运行所有论文实验的脚本
根据论文和README，运行所有基线模型和M3FEND的实验
"""
import os
import subprocess
import sys
import json
from datetime import datetime

# 模型配置：模型名称和学习率
MODEL_CONFIGS = {
    'textcnn': 0.0007,
    'bigru': 0.0009,
    'bert': 7e-5,
    'stylelstm': 0.0007,
    'dualemotion': 0.0009,
    'eann': 0.0001,
    'eddfn': 0.0007,
    'mdfend': 7e-5,
    'm3fend': 0.0001,
    # 注意：mmoe和mose在README中没有明确的学习率，使用默认值
    'mmoe': 0.0001,
    'mose': 0.0001,
}

# 实验配置
EXPERIMENTS = [
    # 中文数据集
    {'dataset': 'ch', 'domain_num': 3, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
    {'dataset': 'ch', 'domain_num': 6, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
    {'dataset': 'ch', 'domain_num': 9, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
    # 英文数据集
    {'dataset': 'en', 'domain_num': 3, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
]

def run_experiment(dataset, domain_num, model_name, gpu='0', epoch=50):
    """运行单个实验"""
    lr = MODEL_CONFIGS.get(model_name, 0.0001)
    
    cmd = [
        sys.executable, 'main.py',
        '--gpu', str(gpu),
        '--lr', str(lr),
        '--model_name', model_name,
        '--dataset', dataset,
        '--domain_num', str(domain_num),
        '--epoch', str(epoch)
    ]
    
    print(f"\n{'='*80}")
    print(f"运行实验: {model_name} | 数据集: {dataset} | 领域数: {domain_num} | 学习率: {lr}")
    print(f"{'='*80}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(cmd, cwd='M3FEND-main', check=True, 
                              capture_output=False, text=True)
        print(f"\n✓ 实验完成: {model_name} | {dataset} | domain_num={domain_num}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 实验失败: {model_name} | {dataset} | domain_num={domain_num}")
        print(f"错误: {e}\n")
        return False

def main():
    """主函数：运行所有实验"""
    print("="*80)
    print("M3FEND 论文实验复现脚本")
    print("="*80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    results = []
    total_experiments = sum(len(exp['models']) for exp in EXPERIMENTS)
    current = 0
    
    for exp_config in EXPERIMENTS:
        dataset = exp_config['dataset']
        domain_num = exp_config['domain_num']
        
        for model_name in exp_config['models']:
            current += 1
            print(f"\n进度: {current}/{total_experiments}")
            
            success = run_experiment(
                dataset=dataset,
                domain_num=domain_num,
                model_name=model_name,
                gpu='0',
                epoch=50
            )
            
            results.append({
                'dataset': dataset,
                'domain_num': domain_num,
                'model': model_name,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
    
    # 保存结果摘要
    summary = {
        'total': total_experiments,
        'success': sum(1 for r in results if r['success']),
        'failed': sum(1 for r in results if not r['success']),
        'results': results,
        'end_time': datetime.now().isoformat()
    }
    
    summary_file = 'M3FEND-main/experiment_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("所有实验完成!")
    print("="*80)
    print(f"总计: {total_experiments} 个实验")
    print(f"成功: {summary['success']} 个")
    print(f"失败: {summary['failed']} 个")
    print(f"结果摘要已保存到: {summary_file}")
    print("="*80)
    
    # 打印失败的实验
    failed = [r for r in results if not r['success']]
    if failed:
        print("\n失败的实验:")
        for r in failed:
            print(f"  - {r['model']} | {r['dataset']} | domain_num={r['domain_num']}")

if __name__ == '__main__':
    main()
