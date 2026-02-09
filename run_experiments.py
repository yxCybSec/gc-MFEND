"""
M3FEND 论文实验运行脚本
支持运行单个实验或批量运行所有实验
"""
import os
import subprocess
import sys
import json
import argparse
from datetime import datetime

# 模型配置：模型名称和学习率（根据README）
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
    'mmoe': 0.0001,
    'mose': 0.0001,
}

def run_single_experiment(dataset, domain_num, model_name, gpu='0', epoch=50, lr=None):
    """运行单个实验"""
    if lr is None:
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
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✓ 实验完成: {model_name} | {dataset} | domain_num={domain_num}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 实验失败: {model_name} | {dataset} | domain_num={domain_num}")
        print(f"错误: {e}\n")
        return False

def run_all_experiments(gpu='0', epoch=50):
    """运行所有论文实验"""
    experiments = [
        # 中文数据集
        {'dataset': 'ch', 'domain_num': 3, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
        {'dataset': 'ch', 'domain_num': 6, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
        {'dataset': 'ch', 'domain_num': 9, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
        # 英文数据集
        {'dataset': 'en', 'domain_num': 3, 'models': ['m3fend', 'mdfend', 'eann', 'eddfn', 'bert', 'bigru', 'textcnn', 'dualemotion', 'stylelstm', 'mmoe', 'mose']},
    ]
    
    results = []
    total = sum(len(exp['models']) for exp in experiments)
    current = 0
    
    print("="*80)
    print("开始运行所有论文实验")
    print("="*80)
    print(f"总计: {total} 个实验")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    for exp_config in experiments:
        dataset = exp_config['dataset']
        domain_num = exp_config['domain_num']
        
        for model_name in exp_config['models']:
            current += 1
            print(f"\n进度: {current}/{total}")
            
            success = run_single_experiment(
                dataset=dataset,
                domain_num=domain_num,
                model_name=model_name,
                gpu=gpu,
                epoch=epoch
            )
            
            results.append({
                'dataset': dataset,
                'domain_num': domain_num,
                'model': model_name,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
    
    # 保存结果
    summary = {
        'total': total,
        'success': sum(1 for r in results if r['success']),
        'failed': sum(1 for r in results if not r['success']),
        'results': results,
        'end_time': datetime.now().isoformat()
    }
    
    summary_file = 'experiment_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("所有实验完成!")
    print("="*80)
    print(f"总计: {total} 个实验")
    print(f"成功: {summary['success']} 个")
    print(f"失败: {summary['failed']} 个")
    print(f"结果摘要已保存到: {summary_file}")
    print("="*80)

def run_m3fend_only(gpu='0', epoch=50):
    """只运行M3FEND的主要实验"""
    experiments = [
        {'dataset': 'ch', 'domain_num': 3},
        {'dataset': 'ch', 'domain_num': 6},
        {'dataset': 'ch', 'domain_num': 9},
        {'dataset': 'en', 'domain_num': 3},
    ]
    
    print("="*80)
    print("运行M3FEND主要实验")
    print("="*80)
    
    for exp in experiments:
        run_single_experiment(
            dataset=exp['dataset'],
            domain_num=exp['domain_num'],
            model_name='m3fend',
            gpu=gpu,
            epoch=epoch
        )
    
    print("\n" + "="*80)
    print("M3FEND实验完成!")
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description='运行M3FEND论文实验')
    parser.add_argument('--mode', choices=['single', 'all', 'm3fend'], default='single',
                       help='运行模式: single(单个实验), all(所有实验), m3fend(只运行M3FEND)')
    parser.add_argument('--dataset', choices=['ch', 'en'], default='ch',
                       help='数据集: ch(中文) 或 en(英文)')
    parser.add_argument('--domain_num', type=int, default=3,
                       help='领域数量: 中文可选3/6/9, 英文只能选3')
    parser.add_argument('--model', default='m3fend',
                       help='模型名称')
    parser.add_argument('--gpu', default='0', help='GPU索引')
    parser.add_argument('--epoch', type=int, default=50, help='训练轮数')
    parser.add_argument('--lr', type=float, default=None, help='学习率(默认使用推荐值)')
    
    args = parser.parse_args()
    
    if args.mode == 'single':
        run_single_experiment(
            dataset=args.dataset,
            domain_num=args.domain_num,
            model_name=args.model,
            gpu=args.gpu,
            epoch=args.epoch,
            lr=args.lr
        )
    elif args.mode == 'all':
        run_all_experiments(gpu=args.gpu, epoch=args.epoch)
    elif args.mode == 'm3fend':
        run_m3fend_only(gpu=args.gpu, epoch=args.epoch)

if __name__ == '__main__':
    main()
