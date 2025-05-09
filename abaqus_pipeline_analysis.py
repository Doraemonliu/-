import os
import csv
from abaqus import *
from abaqusConstants import *


def import_solidworks_model(model_path):
    """
    导入SolidWorks模型文件
    :param model_path: SolidWorks模型文件路径(.sldprt或.step)
    :return: Abaqus模型对象
    """
    try:
        # 创建新的Abaqus模型
        model_name = os.path.splitext(os.path.basename(model_path))[0]
        my_model = mdb.Model(name=model_name)
        
        # 导入SolidWorks模型
        session.openOdb(model_path)
        part = my_model.PartFromGeometryFile(
            name='pipeline_part',
            geometryFile=model_path,
            combine=True
        )
        
        return my_model
    except Exception as e:
        print(f"导入SolidWorks模型失败: {str(e)}")
        return None


def setup_fatigue_analysis(model, load_conditions):
    """
    设置疲劳分析参数
    :param model: Abaqus模型对象
    :param load_conditions: 载荷条件字典
    :return: 分析作业对象
    """
    try:
        # 创建材料属性
        material = model.Material(name='PipeMaterial')
        material.Elastic(table=((210000, 0.3),))  # 钢的弹性模量和泊松比
        
        # 创建截面属性并分配给部件
        section = model.HomogeneousSolidSection(
            name='PipeSection', 
            material='PipeMaterial', 
            thickness=1.0
        )
        
        # 创建分析步
        model.StaticStep(
            name='FatigueAnalysis', 
            previous='Initial',
            description='Fatigue analysis of pipeline'
        )
        
        # 设置载荷和边界条件
        # 这里添加具体的载荷和边界条件代码
        
        # 创建并返回分析作业
        job = mdb.Job(
            name='PipelineFatigueAnalysis',
            model=model.name,
            description='Fatigue analysis of pipeline model'
        )
        
        return job
    except Exception as e:
        print(f"设置疲劳分析失败: {str(e)}")
        return None


def run_analysis_and_export_results(job, output_csv_path):
    """
    运行分析并导出结果到CSV
    :param job: 分析作业对象
    :param output_csv_path: 输出CSV文件路径
    :return: 是否成功
    """
    try:
        # 提交分析作业
        job.submit()
        job.waitForCompletion()
        
        # 获取分析结果
        odb = session.openOdb(job.name + '.odb')
        stress_field = odb.steps['FatigueAnalysis'].frames[-1].fieldOutputs['S']
        
        # 将结果写入CSV
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Node', 'S11', 'S22', 'S33', 'S12', 'S13', 'S23'])
            
            for value in stress_field.values:
                writer.writerow([
                    value.nodeLabel,
                    value.data[0],  # S11
                    value.data[1],  # S22
                    value.data[2],  # S33
                    value.data[3],  # S12
                    value.data[4],  # S13
                    value.data[5]   # S23
                ])
        
        print(f"分析结果已成功导出到: {output_csv_path}")
        return True
    except Exception as e:
        print(f"分析运行或结果导出失败: {str(e)}")
        return False


if __name__ == "__main__":
    # 配置路径
    input_model = "pipeline_model.sldprt"  # SolidWorks模型文件路径
    output_csv = "fatigue_analysis_results.csv"  # 结果输出文件路径
    
    # 1. 导入模型
    model = import_solidworks_model(input_model)
    if model is None:
        exit(1)
    
    # 2. 设置分析参数
    load_conditions = {
        'pressure': 10.0,  # MPa
        'temperature': 20.0  # °C
    }
    job = setup_fatigue_analysis(model, load_conditions)
    if job is None:
        exit(1)
    
    # 3. 运行分析并导出结果
    if not run_analysis_and_export_results(job, output_csv):
        exit(1)