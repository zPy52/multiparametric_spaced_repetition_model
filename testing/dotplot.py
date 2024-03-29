from typing import List, Tuple
from collections import namedtuple

import matplotlib.pyplot as _plt

DotPoint = namedtuple('DotPoint', ('x', 'ymax', 'ydot', 'ymin'))

class DotPlot:
    def __init__(self, dot_points: List[DotPoint] | Tuple[DotPoint], color: str = 'royalblue', factor: float = 0.075):
        _plt.figure()
        
        x = []
        ymaxes = []
        ydots = []
        ymins = []
        
        for dot_point in dot_points:
            if not isinstance(dot_point, DotPoint):
                raise TypeError('Invalid DotPoint object found in the passed list or tuple.')
            
            x.append(dot_point.x)
            ymaxes.append(dot_point.ymax)
            ydots.append(dot_point.ydot)
            ymins.append(dot_point.ymin)
        
        _plt.scatter(x, ydots, color=color)
        
        for n in range(len(x)):
            _plt.vlines(x=x[n], ymin=ymins[n], ymax=ymaxes[n], color=color)
            
            _plt.plot([x[n] - factor, x[n] + factor], [ymaxes[n], ymaxes[n]], color=color)
            _plt.plot([x[n] - factor, x[n] + factor], [ymins[n], ymins[n]], color=color)
        
    
    def plot(self, x: list | tuple, y: list | tuple, style: str = '-', color: str ='royalblue'):
        _plt.plot(x, y, style, color=color)
    
    def title(self, title: str):
        _plt.title(title)
    
    def xlabel(self, xlabel: str):
        _plt.xlabel(xlabel)
    
    def ylabel(self, ylabel: str):
        _plt.ylabel(ylabel)
    
    def show(self):
        _plt.show()
        
    def savefig(self, filename: str, format: str = 'png', dpi: int =300):
        _plt.savefig(filename, format=format, dpi=dpi)

if __name__ == '__main__':
    mae_2__1_5 = 0.10210263279743802
    
    mae = {
    '0.5': {'0.5': 0.10259873323076397, '5.0': 0.10426873729664934, '10.0': 0.10426873729664934, '15.0': 0.10426873729664934}, #'20.0': nan, '25.0': nan, '30.0': nan}, 
    '5.0': {'0.5': 0.10202005286254609, '5.0': 0.10203889000312351, '10.0': 0.10225560577183049, '15.0': 0.10309995927804774, '20.0': 0.10351002907997704, '25.0': 0.10352772651493515, '30.0': 0.10352792705354517}, 
    '10.0': {'0.5': 0.1020110288197325, '5.0': 0.10201165893963467, '10.0': 0.10201570512626197, '15.0': 0.10203420294689003, '20.0': 0.10210618982395647, '25.0': 0.10233521061677354, '30.0': 0.10279107399392824}, 
    '15.0': {'0.5': 0.10201038097294123, '5.0': 0.10201035556371059, '10.0': 0.10201048004565656, '15.0': 0.10201148329924123, '20.0': 0.10201544921359738, '25.0': 0.10202829187242923, '30.0': 0.10206375753772245}, 
    '20.0': {'0.5': 0.1020109067101257, '5.0': 0.10201084623687892, '10.0': 0.10201064684910462, '15.0': 0.10201038699937548, '20.0': 0.1020104654846017, '25.0': 0.10201144692739814, '30.0': 0.10201470386488527}, 
    '25.0': {'0.5': 0.10201136906978202, '5.0': 0.10201132374194911, '10.0': 0.10201118659145939, '15.0': 0.1020109882764891, '20.0': 0.10201070693460729, '25.0': 0.1020103908009326, '30.0': 0.10201045965514402}, 
    '30.0': {'0.5': 0.10201180543855487, '5.0': 0.10201176912537123, '10.0': 0.10201167255806803, '15.0': 0.10201150290197941, '20.0': 0.10201127950282626, '25.0': 0.10201101645021989, '30.0': 0.10201071184090535}
    }
    
    auc_2__1_5 = 0.5137041703681645
    
    auc = {
    '0.5': {'0.5': 0.5121434625729784, '5.0': 0.5002166421431185, '10.0': 0.49461467738279036, '15.0': 0.49461467738279036, '20.0': 0.49461467738279036, '25.0': 0.49461467738279036, '30.0': 0.49461467738279036}, 
    '5.0': {'0.5': 0.5143833435034102, '5.0': 0.5143799505221434, '10.0': 0.5134531158724593, '15.0': 0.5104435398473675, '20.0': 0.5090497456153954, '25.0': 0.5082725925809394, '30.0': 0.5073571856322356}, 
    '10.0': {'0.5': 0.514506802865747, '5.0': 0.5144700544547486, '10.0': 0.5143947274788471, '15.0': 0.514366036737832, '20.0': 0.5138150033818778, '25.0': 0.5132061955013535, '30.0': 0.5113446097976403}, 
    '15.0': {'0.5': 0.5145763029668615, '5.0': 0.5146047273010811, '10.0': 0.5145847230819174, '15.0': 0.5144371321661769, '20.0': 0.5145259055167302, '25.0': 0.5144747118954025, '30.0': 0.5142649899710067}, 
    '20.0': {'0.5': 0.5147181045583332, '5.0': 0.5146401635965357, '10.0': 0.5146634336550717, '15.0': 0.514574702321445, '20.0': 0.5145632221363635, '25.0': 0.5144318727928614, '30.0': 0.5146026535192837}, 
    '25.0': {'0.5': 0.5148108334067744, '5.0': 0.514749468739026, '10.0': 0.514700272800622, '15.0': 0.5147598813012493, '20.0': 0.5146580478781172, '25.0': 0.5145787695229401, '30.0': 0.5145619077156697}, 
    '30.0': {'0.5': 0.5147964807155354, '5.0': 0.514677714461494, '10.0': 0.5146663318851994, '15.0': 0.514751922459873, '20.0': 0.5146766101391725, '25.0': 0.5147459936299205, '30.0': 0.5146361044428195}
    }
    
    dots = []
    
    # Can be 'MAE' or 'AUC'.
    mode = 'AUC'
    
    data = mae if mode == 'MAE' else auc
    
    for n in data:
        top_k, top_v = max(data[n].items(), key=lambda x: x[1])
        
        bottom_k, bottom_v = min(data[n].items(), key=lambda x: x[1])
        
        mid_v = (top_v + bottom_v) / 2
        
        dots.append(DotPoint(float(n), top_v, mid_v, bottom_v))
    
    dplt = DotPlot(dots, factor=0.35)
        
    dplt.title(f'({"A" if mode == "MAE" else "B"}) {mode} Variation')
    dplt.ylabel(f'{mode} due to β')
    dplt.xlabel('α and γ')
        
    dplt.plot([0.5, 30.0], [mae_2__1_5 if mode == 'MAE' else auc_2__1_5] * 2, style='-.', color='black')
    
    dplt.savefig(f'testing/{mode}_plot.jpg', format='jpg', dpi=1_000)
    
    dplt.show()