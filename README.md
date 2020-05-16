# electric-field
电场线根据电场强度分布的电场线

## 起因

由于matplotlib的streamplot实现不尽人意，且大多是矢量流图布局的结果大多不是真实的按场强分布，而是均匀分布，所以重新编写了关于接地线的分布布局

## 效果

1. 最简单的情况异种电荷的电场线分布

<img src="https://github.com/moyuwangzi/electric-field/blob/master/images/-1%E3%80%811.jpg" alt="-1、1" title="异种对称电荷电场线分布" style="zoom:80%;" />

2. <img src="https://github.com/moyuwangzi/electric-field/blob/master/images/-5%E3%80%811.jpg" alt="-5、1" title="5，-1" style="zoom:50%;" /> <img src="https://github.com/moyuwangzi/electric-field/blob/master/images/-1%E3%80%815.jpg" alt="my-logo.png" title="-1，5" style="zoom:50%;" />

3. 四等量异种电荷电场分布图

   <img src="https://github.com/moyuwangzi/electric-field/blob/master/images/-1%E3%80%811%E3%80%811%E3%80%81-1.jpg" alt="-1、1、1、-1" style="zoom:50%;" />

   <img src="https://github.com/moyuwangzi/electric-field/blob/master/images/-1%E3%80%811%E3%80%81-1%E3%80%811.jpg" alt="-1、1、-1、1" style="zoom:50%;" />

4. 非等量异种电荷电场分布图

   <img src="https://github.com/moyuwangzi/electric-field/blob/master/images/-1%E3%80%81-1%E3%80%81-1%E3%80%813.jpg" alt="-1、-1、-1、3" style="zoom:80%;" />

## 总结

在等量电荷的时候较为真实，然而在异量电荷的分布，依旧不够真实

此阶段，虽然可以花更多的线和时间来进行进一步拟合，但与付出的计算资源不成正比

由于花费时间较短，算法比较简陋，修正后精度应该还会上升
