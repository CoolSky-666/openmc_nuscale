
import openmc
import matplotlib.pyplot as plt
import pandas as pd  # 导入 pandas 库
import numpy as np
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter
import matplotlib.font_manager as fm

statepoint_filename = 'statepoint.300.h5'  # 示例文件名，根据实际情况修改
sp = openmc.StatePoint(statepoint_filename)

power = 160e6 # 160 MW [J/s]
# 提取第一个 tally（rad_pow）的结果
t1 = sp.get_tally(name='rad_pow') # Tally类
t2 = sp.get_tally(name='pin_pow')
t3 = sp.get_tally(name='pow_ax')


t1_mean = t1.mean*37 / np.sum(t1.mean)
t1_std = t1.std_dev*37 / np.sum(t1.mean)
t2_mean = t2.mean*power / np.sum(t2.mean)
t2_std = t2.std_dev*power / np.sum(t2.mean)
t3_mean = t3.mean*160 / np.sum(t3.mean)
t3_std = t3.std_dev*160 / np.sum(t3.mean)

# 把顺序翻转过来
rad_mean = t1_mean.reshape((7,7))[::-1]
rad_std = t1_std.reshape((7,7))[::-1]
pin_mean = t2_mean.reshape((7*17,7*17))[::-1]
pin_std = t2_std.reshape((7*17,7*17))[::-1]
ax_mean = np.squeeze(t3_mean)
ax_std = np.squeeze(t3_std)

# 将 0 替换为 NaN
rad_mean[rad_mean == 0] = np.nan
rad_std[rad_std == 0] = np.nan
pin_mean[pin_mean == 0] = np.nan
pin_std[pin_std == 0] = np.nan

# ==================> 一、极向功率(rad_pow)热力图 <==================
plt.figure(figsize=(10, 8))
# 绘制热力图
print(rad_mean)
sns.heatmap(rad_mean.reshape((7,7)), annot=True, fmt=".3f", cmap="autumn_r", cbar=True, mask=np.isnan(rad_mean),linewidths=0, linecolor='black', annot_kws={"size": 14})  # 设置热力图注释文字大小
plt.xticks(ticks=np.arange(7) + 0.5, labels=list('ABCDEFG'), minor=False, fontsize=14)  # 设置 X 轴标签大小
plt.yticks(ticks=np.arange(7) + 0.5, labels=list('1234567'), minor=False, fontsize=14)  # 设置 Y 轴标签大小
# 去除 X 轴和 Y 轴的刻度线
plt.tick_params(axis='x', which='both', length=0)
plt.tick_params(axis='y', which='both', length=0)
# 设置标签旋转角度
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.savefig('1-rad_pow.png', format='png', dpi=300)
print("==========> 极向功率(rad_pow)热力图 <==========")

# ==================> 二、燃料棒极向功率(rad_pow)热力图 <==================
print("==========> 燃料棒极向功率(rad_pow)热力图 <==========")
plt.figure(figsize=(10, 8))
ax = sns.heatmap(pin_mean,fmt=".3f", cmap='jet')
cbar = ax.collections[0].colorbar
cbar.formatter = FormatStrFormatter('%.1e')  # 设置科学计数法格式，保留一位小数
plt.xticks([])
plt.yticks([])
pic_name = '2-pin_pow.png'
print(f"图片文件已保存到{pic_name}")
plt.savefig(pic_name, format='png', dpi=300)
plt.clf()


# ==================> 三、轴向功率(ax_pow)热力图 <==================
height = np.array([11.365,14.920,19.365,31.017,42.670,54.322,65.974,70.419,82.071,93.724,105.376,117.028,121.473,133.125,144.778,156.430,168.082,172.527,182.236,191.946,201.656,211.365])
power = np.append(ax_mean,ax_mean[-1])
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xticks(height)
ax.set_xticklabels(height)
# 绘制阶梯图
ax.step(height,power,where='post',linewidth=1,label='Axis power',color='blue')
grid_x = [168.082,121.473,117.028,70.419,65.974,19.365,14.92]
ax.axvline(x=172.527, color='red', linestyle='--',linewidth=1, label=f'Spacer grid')
for pos in grid_x:
    ax.axvline(x=pos, color='red', linestyle='--',linewidth=1)
ax.set_xlabel('高度 (cm)',  fontproperties=font_prop)
ax.set_ylabel('功率 (MW)', fontproperties=font_prop)
plt.xticks(rotation=45)
ax.legend()
ax.grid(True)
plt.savefig('3-ax_pow.png', format='png', dpi=300)
plt.clf()
