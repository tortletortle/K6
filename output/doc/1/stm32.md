# 新建project:

## 目录

- [新建project:](#新建project)
  - [GPIO](#gpio)
  - [延时函数和OLED函数](#延时函数和oled函数)
  - [五. 注意事项:](#五-注意事项)
  - [函数封装:](#函数封装)
  - [外部中断](#外部中断)
  - [定时器](#定时器)
  - [ADC](#adc)
  - [DMA](#dma)
  - [USART串口外设](#usart串口外设)
  - [I2C](#i2c)
  - [SPI](#spi)
  - [BKP](#bkp)
  - [RTC](#rtc)
  - [PWR](#pwr)
  - [看门狗](#看门狗)

### 基本文件

单片机型号:

Start的启动文件:

library的启动文件:

User文件夹的启动文件:

添加头文件路径:

1. 输入函数时的格式显示:

1. 硬件调试时立即执行,否则按一下复位键

1. 添加库函数

添加到USER的程序

## GPIO

开启时钟:RCC\_APB2PeriphClockCmd(RCC\_APB2Periph\_GPIOB,ENABLE);

如果是一个指针,那前面要加一个取地址的符号&

高低电平

添加结构体:

GPIO\_Mode\_AIN = 0x0,模拟输入,ADC使用

GPIO\_Mode\_IN\_FLOATING = 0x04,浮空输入

GPIO\_Mode\_IPD = 0x28,下拉输入,按键按下时端口接低电平

GPIO\_Mode\_IPU = 0x48,上拉输入,按键未按下时端口接高电平

GPIO\_Mode\_Out\_OD = 0x14,开漏输出(输出要外接5V电源时或低电平输出使用,此时注意应使用对5V容忍的IO口),输出低电平,强下拉;输出高电平,引脚处于浮空;开漏输出模式下,仍然可以输入,输入时,先输出1,再直接读取输入数据寄存器就行了

GPIO\_Mode\_Out\_PP = 0x10,推挽输出(外设直接输出3.3V时或低电平输出使用)

GPIO\_Mode\_AF\_OD = 0x1C,复用开漏输出

GPIO\_Mode\_AF\_PP = 0x18,复用推免输出(将输出控制权交给片上外设时使用,比如定时器,串口)

GPIO\_Init()初始化端口

单独设置某个端口

GPIO\_Setbits(GPIOA,GPIO\_Pin\_0),拉高引脚输出电平

GPIO\_ResetBits(GPIOA,GPIO\_Pin\_0),拉低引脚输出电平

GPIO\_WriteBit(GPIOA,GPIO\_Pin\_0,Bit\_SET);

读取输入输出:

uint8\_t GPIO\_ReadInputDataBit(GPIO\_TypeDef\* GPIOx, uint16\_t GPIO\_Pin);读取其中一个端口

uint16\_t GPIO\_ReadInputData(GPIO\_TypeDef\* GPIOx);读取整个端口(16位)

uint8\_t GPIO\_ReadOutputDataBit(GPIO\_TypeDef\* GPIOx, uint16\_t GPIO\_Pin);读取输出位

uint16\_t GPIO\_ReadOutputData(GPIO\_TypeDef\* GPIOx);

### 重映射:

重映射关系看端口表,GPIO\_PinRemapConfig的第一个参数看手册里的8.3

以TIM2为例如下:

RCC\_APB2PeriphClockCmd(RCC\_APB2Periph\_AFIO,ENABLE);启用AFIO

GPIO\_PinRemapConfig(GPIO\_PartialRemap1\_TIM2,ENABLE);启用TIM2的重映射

GPIO\_PinRemapConfig(GPIO\_Remap\_SWJ\_JTAGDisable,ENABLE);将PA15原来的调试端口功能去除

## 延时函数和OLED函数

添加到System文件夹

main函数加上#include "Delay.h"

void Delay\_us(uint32\_t us);微秒

void Delay\_ms(uint32\_t ms);毫秒

void Delay\_s(uint32\_t s);秒

OLED函数

## 五. 注意事项:

1. PA15,PB3,PB4一般不用做普通端口

如果PA15要拿来当端口用,则需要关闭它初始的调试端口功能,看端口表看对应的调试端口,比如PA15对应的就是JTDI

调试端口:比如全部取消掉之后,再使用STlink就下载不进去程序,就只能使用串口下载,下载一个新的调试端口的程序.

GPIO\_PinRemapConfig(GPIO\_Remap\_SWJ\_JTAGDisable,ENABLE);可以去除调试端口功能

GPIO\_Remap\_SWJ\_JTAGDisable参数对应解除的调试端口:

GPIO\_Remap\_SWJ\_NoJTRST参数对应解除的调试端口:

GPIO\_Remap\_SWJ\_Disable:(清除全部调试端口,谨慎使用)

1. 代码提示框:“CTRL +ALT+ 空格”

1. 宏定义:

复制

粘贴到这里

1. 在函数里面的是局部变量,在函数外面的是全局变量。在函数内部,优先使用自己的局部变量。
1. C语言不能写二进制,要用16进制的写法
1. new state翻译:返回值
1. 跨文件使用变量,要在头部声明:eg:extern uint16\_t Num;
1. 不同的GPIO口对应的输出比较通道对照:

1. %取余只能对整数进行操作
1. float 类型属于浮点类型,显示小数点后两位
1.
1. const 用于将大量不需要更改的数据存储在flash里而不占用SRAM的内存.
1. 不涉及外围硬件电路的程序可以添加到System里;涉及硬件外围电路的程序添加到Hardware里
1. 结构体名称可以作为地址,指向该结构体的第一个元素
1. 可以在.h文件里声明一个可调用的变量,用extern
1. 尽量用多个外设互相联系互相交织,而不是一个CPU单独地控制多个外设,如此可以节约CPU资源
1. C语言中没有专门的字符串变量,通常用一个[字符数组](https://so.csdn.net/so/search?q=%E5%AD%97%E7%AC%A6%E6%95%B0%E7%BB%84&spm=1001.2101.3001.7020)来存放一个字符串,字符串总是以【'\\0'】作为结束符。
1. 要用printf,sprintf函数时,要操作:
,并在开头写入#include <stdio.h>

1. 包含汉子的字符串功能开启:在魔术棒中写入--no-multibyte-chars

1. static 静态变量,在函数内部初始化之后,离开函数,值仍保留
1. 程序中出现大量的while等循环时,如果有其中一个while没有退出循环,那程序会卡死,因此有必要加上超时退出机制:
uint32\_t Timeout;

Timeout = 10000;

while (I2C\_CheckEvent(I2C2,I2C\_EVENT\_MASTER\_MODE\_SELECT) != SUCCESS )

{

Timeout--;

if(Timeout == 0)

{

break;

}

}

1. C语言中,在数字面前不要加0,因为以0开头表示八进制
## 函数封装:

1. 新建一个“.h”文件
(函数均大写)

1. 新建一个.c文件

## 外部中断

外部中断原理图:

其中,AFIO和GPIO的时钟要开启,但是EXTI和NVIC的时钟是一直开启的,所以不需要在初始化中去开启。

void GPIO\_AFIODeInit(void);复位AFIO的配置,使配置全部清除

void GPIO\_PinLockConfig(GPIO\_TypeDef\* GPIOx, uint16\_t GPIO\_Pin);锁定GPIO外设的配置,防止意外更改.

void GPIO\_PinRemapConfig(uint32\_t GPIO\_Remap, FunctionalState NewState);引脚重映射

void GPIO\_EXTILineConfig(uint8\_t GPIO\_PortSource, uint8\_t GPIO\_PinSource);配置AFIO的数据选择器.选择想要的中断引脚(此处完成第三步),注意这里的引脚参数不能够用”\|”,一次只能配置一个

EXTI的库函数:

void EXTI\_DeInit(void);把EXTI的全部配置清除,恢复成上电默认的状态

void EXTI\_Init(EXTI\_InitTypeDef\* EXTI\_InitStruct);和GPIO\_Init一样

void EXTI\_StructInit(EXTI\_InitTypeDef\* EXTI\_InitStruct);把参数传递的结构体变量赋一个默认值

void EXTI\_GenerateSWInterrupt(uint32\_t EXTI\_Line);用软件触发外部中断

FlagStatus EXTI\_GetFlagStatus(uint32\_t EXTI\_Line);获取指定的标志位是否置1(主程序用)

void EXTI\_ClearFlag(uint32\_t EXTI\_Line);对置1的标志位进行清除(主程序用)

ITStatus EXTI\_GetITStatus(uint32\_t EXTI\_Line);获取中断标志位是否被置1(中断函数里用)

void EXTI\_ClearITPendingBit(uint32\_t EXTI\_Line);清除中断挂起标志位(中断函数里用)

EXTI\_Mode\_Interrupt ,中断模式

EXTI\_Mode\_Event ,事件模式

EXTI的初始化配置:

NVIC的库函数:

void NVIC\_PriorityGroupConfig();用来中断分组(该函数整个芯片只能分组一次,所以只需要第一次分组时运行这个函数,之后的中断都不需要.或者之后的中断函数的分组保持一致)

void NVIC\_Init();初始化NVIC

void NVIC\_SetVectorTable();设置中断向量表

void NVIC\_SystemLPConfig();系统低功耗配置

NVIC\_InitTypeDef NVIC\_InitStructure;

NVIC\_InitStructure.NVIC\_IRQChannel = EXTI15\_10\_IRQn ;从找到里的一个参数,这里指EXTI10-15都用这个参数.

NVIC\_InitStructure.NVIC\_IRQChannelCmd = ENBALE

NVIC\_InitStructure.NVIC\_IRQChannelPreemptionPriority =注意看分组,然后设置抢占优先级和响应由县级

NVIC\_InitStructure.NVIC\_IRQChannelSubPriority = 如上

中断函数:

去文件夹里找到

”IRQHandler”

中断函数不需要在”.h”文件夹里声明,他是自动调用的!

中断函数尽量不要执行耗时的代码,比如Delay函数,而如果想要避免抖动,那就再判断一次引脚电平.eg:

中断函数和主函数尽量不要用同一个硬件

## 定时器

定时器的库函数:

void TIM\_DeInit();恢复初始设置

TIM\_TimeBaseInitTypeDef创建时基单元结构体

void TIM\_TimeBaseInit()时基单元初始化

Tim\_TimeBaseInitStructure.TIM\_ClockDivision =TIM\_CKD\_DIV1 ;时基单元预分频为1

Tim\_TimeBaseInitStructure.TIM\_CounterMode = TIM\_CounterMode\_Up ;向上计数

Tim\_TimeBaseInitStructure.TIM\_Period = 10000 - 1 ;周期(ARR的值)

Tim\_TimeBaseInitStructure.TIM\_Prescaler = 7200 - 1 ;预分频器(PSC的值)

Tim\_TimeBaseInitStructure.TIM\_RepetitionCounter = 0;ARR

void TIM\_BDTRConfig(TIM\_TypeDef\* TIMx, TIM\_BDTRInitTypeDef \*TIM\_BDTRInitStruct);

void TIM\_TimeBaseStructInit(t);赋予结构体一个默认值

void TIM\_BDTRStructInit(TIM\_BDTRInitTypeDef\* TIM\_BDTRInitStruct);

void TIM\_Cmd(;使能计数器(运行控制)

void TIM\_ITConfig();使能中断输出信号(中断输出控制)

void TIM\_GenerateEvent(TIM\_TypeDef\* TIMx, uint16\_t TIM\_EventSource);

void TIM\_DMAConfig(TIM\_TypeDef\* TIMx, uint16\_t TIM\_DMABase, uint16\_t TIM\_DMABurstLength);

void TIM\_DMACmd(TIM\_TypeDef\* TIMx, uint16\_t TIM\_DMASource, FunctionalState NewState);

void TIM\_InternalClockConfig();选择内部时钟

void TIM\_ITRxExternalClockConfig();选择ITRX其它定时器

void TIM\_TIxExternalClockConfig()选择Tix捕获通道的时钟

void TIM\_ETRClockMode1Config()选择ETR通过外部时钟模式1输入的时钟

void TIM\_ETRClockMode2Config()选择ETR通过外部时钟模式2输入的时钟

void TIM\_ETRConfig();单独配置ETR引脚的预分频器/极性/滤波器参数

void TIM\_PrescalerConfig);单独写预分频值的函数

void TIM\_CounterModeConfig();改变计数器的技术模式

void TIM\_ARRPreloadConfig();自动重装器预装功能配置

void TIM\_SelectCOM(TIM\_TypeDef\* TIMx, FunctionalState NewState);

void TIM\_SelectCCDMA(TIM\_TypeDef\* TIMx, FunctionalState NewState);

void TIM\_CCPreloadControl(TIM\_TypeDef\* TIMx, FunctionalState NewState);

void TIM\_UpdateDisableConfig(TIM\_TypeDef\* TIMx, FunctionalState NewState);

void TIM\_UpdateRequestConfig(TIM\_TypeDef\* TIMx, uint16\_t TIM\_UpdateSource);

void TIM\_SelectHallSensor(TIM\_TypeDef\* TIMx, FunctionalState NewState);

void TIM\_SelectOnePulseMode(TIM\_TypeDef\* TIMx, uint16\_t TIM\_OPMode);

void TIM\_SetCounter();给计数器单独写入一个值

void TIM\_SetAutoreload();给自动重装器写入一个值

void TIM\_SelectMasterSlaveMode(TIM\_TypeDef\* TIMx, uint16\_t TIM\_MasterSlaveMode);

void TIM\_SetClockDivision();

uint16\_t TIM\_GetCounter();获取当前计数器CNT的值

uint16\_t TIM\_GetPrescaler();获取当前预分频器的值

FlagStatus TIM\_GetFlagStatus();

void TIM\_ClearFlag();清除

ITStatus TIM\_GetITStatus();

void TIM\_ClearITPendingBit();

调用定时器的中断函数:里的”TIM2\_IRQHandler”

TIM\_GetITStatus()获取中断标志位

TIM\_ClearITPendingBit();清除中断标志位

TIM\_ETR的引脚关系

### 定时器中使用外部中断:

时钟源选择:选择外部触发,所以选ETR,选择对应的引脚配置(比如这里用GPIOA0,然后也要记得配置GPIOA0的初始化)好硬件,在计时器的初始化函数里的时钟源选择处用函数,即用ETR的外部时钟模式2.

TIM\_ETRClockMode2Config(TIM2,TIM\_ExtTRGPSC\_OFF,TIM\_ExtTRGPolarity\_NonInverted,0x00);

其中:

TIM\_ExtTRGPolarity\_NonInverted:高电平或上升沿有效

0x00:指滤波器采样频率,参考下表

### CCR

和CCR(输出比较)相关的库函数:

void TIM\_OC1Init();用结构体配置CCR通道1的初始值,这里有4个通道,同一个TIM可以有4个通道,但因为共用一个CNT,所以ARR和PSC是一样的,相位也是同步的,但占空比由各自的CCR决定.

void TIM\_OC2Init();

void TIM\_OC3Init();

void TIM\_OC4Init();

void TIM\_OCStructInit();给输出比较结构体赋予默认值

void TIM\_CtrlPWMOutputs();使用高级定时器输出PWM时需要调用,否则PWM不能正常输出

void TIM\_ForcedOC1Config();给CCR配置强制输出模式

void TIM\_ForcedOC2Config();

void TIM\_ForcedOC3Config();

void TIM\_ForcedOC4Config();

void TIM\_OC1PreloadConfig();配置CCR寄存器的预装功能(影子寄存器):写入的值不会立即生效,而是更新事件了才会生效.(△)

void TIM\_OC2PreloadConfig();

void TIM\_OC3PreloadConfig();

void TIM\_OC4PreloadConfig();

void TIM\_OC1FastConfig();配置CCR快速使能(△)

void TIM\_OC2FastConfig();

void TIM\_OC3FastConfig();

void TIM\_OC4FastConfig();

void TIM\_ClearOC1Ref();外部事件清除REF信号(△)

void TIM\_ClearOC2Ref();

void TIM\_ClearOC3Ref();

void TIM\_ClearOC4Ref();

void TIM\_OC1PolarityConfig();单独设置CCR的极性

void TIM\_OC1NPolarityConfig();单独设置CCR互补通道的极性

void TIM\_OC2PolarityConfig();

void TIM\_OC2NPolarityConfig();

void TIM\_OC3PolarityConfig();

void TIM\_OC3NPolarityConfig();

void TIM\_OC4PolarityConfig();

void TIM\_CCxCmd();单独修改CCR输出使能参数

void TIM\_CCxNCmd();

void TIM\_SelectOCxM();选择CCR输出比较模式

void TIM\_SetCompare1();单独更改CCR寄存器值

void TIM\_SetCompare2();

void TIM\_SetCompare3();

void TIM\_SetCompare4();

void TIM\_PrescalerConfig);单独写预分频值的函数

CCR初始化(通用定时器需要的参数,高级定时器的话需要配置更多参数)

TIM\_OCInitTypeDef TIM\_OCInitStructure;

TIM\_OCStructInit()给全部结构体参数配置一个初始参数(避免一些不必要的麻烦)

TIM\_OCInitStructure.TIM\_OCMode = ;

TIM\_OCInitStructure.TIM\_OCPolarity = ;

TIM\_OCInitStructure.TIM\_OutputState = ;

TIM\_OCInitStructure.TIM\_Pulse = ;

TIM\_OC1Init(TIM2,&TIM\_OCInitStructure);

OCMode参数:

Pulse:是CCR的值,具体计算公式:

### PWM输入捕获模式&主从触发模式

主从模式和中断触发事件的区别是主从模式不占用软件资源,中断则占用CPU

需要用到的库函数:

void TIM\_ICInit();初始化输入捕获单元,只能配置单通道

void TIM\_PWMIConfig();初始化输入捕获单元,能配置两个通道()PWMI模式)

void TIM\_ICStructInit();

void TIM\_SelectOutputTrigger();选择主模式输出触发源TRGI

void TIM\_SelectInputTrigger(); 选择从模式输入触发源TRGI

void TIM\_SelectSlaveMode();选择从模式

void TIM\_SetIC1Prescaler();单独写入PSC

void TIM\_SetIC2Prescaler();

void TIM\_SetIC3Prescaler();

void TIM\_SetIC4Prescaler();

uint16\_t TIM\_GetCapture1();读取CCR

uint16\_t TIM\_GetCapture2();

uint16\_t TIM\_GetCapture3();

uint16\_t TIM\_GetCapture4();

测频率的方法原理:

其中,Fc=72M/PSC,所以PSC取72,720等;为了不让ARR溢出,让ARR取65536-1

IC初始化部分代码:

TIM\_ICInitStructure.TIM\_Channel = TIM\_Channel\_1; 通道1

TIM\_ICInitStructure.TIM\_ICFilter = 0xF; 滤波

TIM\_ICInitStructure.TIM\_ICPolarity = TIM\_ICPolarity\_Rising; 上升沿有效

TIM\_ICInitStructure.TIM\_ICPrescaler = TIM\_ICPSC\_DIV1; 不分频

TIM\_ICInitStructure.TIM\_ICSelection = TIM\_ICSelection\_DirectTI; 不交叉电路

TIM\_ICInit(TIM3,&TIM\_ICInitStructure);

TIM\_PWMIConfig(TIM3,&TIM\_ICInitStructure); //配置PWMI模式(两通道,仅支持通道1和通道2)

### 定时器编码

需要用到的库函数:

void TIM\_EncoderInterfaceConfig();定时器编码接口配置

TIM\_ICStructInit()

编码器接口大概可以理解成一个带方向的外部时钟;而内置时钟不起作用,因此不需要配置TIM\_InternalClockConfig(TIM2);函数;Tim\_TimeBaseInitStructure.TIM\_CounterMode参数也不起作用

一般TIM\_Period写入65536-1.这样计数范围大而且方便转为负值(不用unit16\_t定义计数值,用int16\_t定义)

TIM\_Prescaler给0;不分频

TIM\_ICInitStructure.TIM\_ICPolarity = TIM\_ICPolarity\_Rising;这个参数不是指上升沿有效,是指TI1不反向

有效边沿一般取TI1和TI2均有效,如此输入比较灵敏.

## ADC

相关的库函数:

void RCC\_ADCCLKConfig(uint32\_t RCC\_PCLK2);配置ADCCLK分频器(只能选6和8),ADCCLK = 72MHZ/6或8

void ADC\_DeInit();恢复配置

void ADC\_Init();

void ADC\_StructInit();

void ADC\_Cmd();使能

void ADC\_DMACmd();开启ADC和DMA传输信号

void ADC\_ITConfig();中断输出控制

void ADC\_ResetCalibration();复位校准

FlagStatus ADC\_GetResetCalibrationStatus();获取复位校准状态

void ADC\_StartCalibration();开始校准

FlagStatus ADC\_GetCalibrationStatus();获取开始校准状态

void ADC\_SoftwareStartConvCmd();软件触发控制

FlagStatus ADC\_GetSoftwareStartConvStatus();没啥用

void ADC\_DiscModeChannelCountConfig();配置间断模式

void ADC\_DiscModeCmd();启用或不启用间断模式

void ADC\_RegularChannelConfig();给各个序列位置填写通道

eg: ADC\_RegularChannelConfig(ADC1,ADC\_Channel\_0,1,ADC\_SampleTime\_55Cycles5);

ADC\_Channel\_0 指哪个通道,可任意修改

第三个参数1,指位置序列第一个

ADC\_SampleTime\_55Cycles5 采样时间的参数,如果需要更快的转换,选择小参数;如果需要更稳定的转换,就选择较大的参数;

void ADC\_ExternalTrigConvCmd();启用或不启用外部触发转换

uint16\_t ADC\_GetConversionValue();获取ADC转换的数据寄存器

uint32\_t ADC\_GetDualModeConversionValue();获取双ADC转换的数据寄存器

void ADC\_AutoInjectedConvCmd();注入组相关函数

void ADC\_InjectedDiscModeCmd();

void ADC\_ExternalTrigInjectedConvConfig();

void ADC\_ExternalTrigInjectedConvCmd(ADC\_TypeDef\* ADCx, FunctionalState NewState);

void ADC\_SoftwareStartInjectedConvCmd(ADC\_TypeDef\* ADCx, FunctionalState NewState);

FlagStatus ADC\_GetSoftwareStartInjectedConvCmdStatus(ADC\_TypeDef\* ADCx);

void ADC\_InjectedChannelConfig(ADC\_TypeDef\* ADCx, uint8\_t ADC\_Channel, uint8\_t Rank, uint8\_t ADC\_SampleTime);

void ADC\_InjectedSequencerLengthConfig(ADC\_TypeDef\* ADCx, uint8\_t Length);

void ADC\_SetInjectedOffset(ADC\_TypeDef\* ADCx, uint8\_t ADC\_InjectedChannel, uint16\_t Offset);

uint16\_t ADC\_GetInjectedConversionValue(ADC\_TypeDef\* ADCx, uint8\_t ADC\_InjectedChannel);

void ADC\_AnalogWatchdogCmd();是否启动模拟看门狗

void ADC\_AnalogWatchdogThresholdsConfig();配置高低阈值

void ADC\_AnalogWatchdogSingleChannelConfig();配置看门通道

void ADC\_TempSensorVrefintCmd();开启ADC温度传感器和内部参考电压控制的通道

FlagStatus ADC\_GetFlagStatus();获取标志位状态,判断转换是否结束

void ADC\_ClearFlag(ADC\_TypeDef\* ADCx, uint8\_t ADC\_FLAG);

ITStatus ADC\_GetITStatus();获取中断状态

void ADC\_ClearITPendingBit();清除中断挂起位

ADC结构体配置:

ADC\_InitStructure.ADC\_ContinuousConvMode = DISABLE;单次还是连续扫描

ADC\_InitStructure.ADC\_DataAlign = ADC\_DataAlign\_Right;左对齐还是右对齐

ADC\_InitStructure.ADC\_ExternalTrigConv = ADC\_ExternalTrigConv\_None;定义外部触发源

ADC\_InitStructure.ADC\_Mode = ADC\_Mode\_Independent;独立模式还是双ADC模式

ADC\_InitStructure.ADC\_NbrOfChannel = 4;有多少道菜

ADC\_InitStructure.ADC\_ScanConvMode = ENABLE;扫描模式还是非扫描模式

ADC\_Init(ADC1,&ADC\_InitStructure);

ADC校准:

ADC\_ResetCalibration(ADC1);

while(ADC\_GetResetCalibrationStatus(ADC1) == SET);

ADC\_StartCalibration(ADC1);

while(ADC\_GetCalibrationStatus(ADC1) == SET);

如果使用多次转换扫描模式实现多通道,要用DMA实现,否则导致数据覆盖从而无法读取数据.

用单次转换非扫描模式也可以实现多通道,只需要每次触发转换之前,手动更改列表第一个位置的通道即可

## DMA

存储器到存储器的转运用软件触发;外设到存储器的转运用硬件触发

DMA转运的三个条件:1.传输计数器大于0;2.触发源有触发信号;3.DMA使能

STM32F108C7DMA资源:DMA1(7个通道)

存储器到存储器的转运不能用自动重装模式

用软件触发时,和ADC不一样,是只能连续地触发,因此用作存储器到存储器转运的情况.目的是达到尽快完成转运.而硬件触发,是需要配置一个等待时机的

写传输计数器时,必须先DMACMD(DISBALE),才能写入.

硬件触发的外设口和通道是一一对应的:

各通道的优先级默认配置是:序号越小,优先级越高,但这个优先级是可以更改的.

转运A到B完成后,存储器A的数据并不会消失,是一种复制转运

库函数:

void DMA\_DeInit();

void DMA\_Init();

void DMA\_StructInit(;

void DMA\_Cmd();

void DMA\_ITConfig();中断输出使能

void DMA\_SetCurrDataCounter(); 给传输计数器写数据

uint16\_t DMA\_GetCurrDataCounter();返回传输计数器的值

FlagStatus DMA\_GetFlagStatus();

void DMA\_ClearFlag();

ITStatus DMA\_GetITStatus();获取中断状态

void DMA\_ClearITPendingBit();清除中断挂起位

结构体参数:

DMA\_InitStructure.DMA\_BufferSize = ;传输计数器

DMA\_InitStructure.DMA\_DIR = ;传输方向

(DMA\_DIR\_PeripheralDST  外设做目的地;DMA\_DIR\_PeripheralSRC外设做源头)

DMA\_InitStructure.DMA\_M2M = ;硬件触发\\软件触发

DMA\_InitStructure.DMA\_MemoryBaseAddr = ;存储器起始地址

DMA\_InitStructure.DMA\_MemoryDataSize = ;存储器数据宽度

DMA\_InitStructure.DMA\_MemoryInc = ;存储器地址是否自增

DMA\_InitStructure.DMA\_Mode = ;是否使用自动重装

DMA\_InitStructure.DMA\_PeripheralBaseAddr = ;外设

DMA\_InitStructure.DMA\_PeripheralDataSize = ;

DMA\_InitStructure.DMA\_PeripheralInc = ;

DMA\_InitStructure.DMA\_Priority = ;优先级

## USART串口外设

TX和RX接口对应GPIO口规则对照引脚手册,但是实物接的时候,TX和RX是相反的.

库函数:

void USART\_DeInit();

void USART\_Init();

void USART\_StructInit();

Void USART\_ClockInit();                    配置同步时钟输出

void USART\_ClockStructInit();

void USART\_Cmd();

void USART\_ITConfig();中断输出使能

void USART\_DMACmd();开启USART到DMA的通道

void USART\_SendData();发送数据(写)

uint16\_t USART\_ReceiveData();接收数据(读)

FlagStatus USART\_GetFlagStatus();

void USART\_ClearFlag();

ITStatus USART\_GetITStatus();获取中断标志位

void USART\_ClearITPendingBit();清除中断标志位

void USART\_SetAddress(USART\_TypeDef\* USARTx, uint8\_t USART\_Address);

void USART\_WakeUpConfig(USART\_TypeDef\* USARTx, uint16\_t USART\_WakeUp);

void USART\_ReceiverWakeUpCmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_LINBreakDetectLengthConfig(USART\_TypeDef\* USARTx, uint16\_t USART\_LINBreakDetectLength);

void USART\_LINCmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_SendBreak(USART\_TypeDef\* USARTx);

void USART\_SetGuardTime(USART\_TypeDef\* USARTx, uint8\_t USART\_GuardTime);

void USART\_SetPrescaler(USART\_TypeDef\* USARTx, uint8\_t USART\_Prescaler);

void USART\_SmartCardCmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_SmartCardNACKCmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_HalfDuplexCmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_OverSampling8Cmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_OneBitMethodCmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

void USART\_IrDAConfig(USART\_TypeDef\* USARTx, uint16\_t USART\_IrDAMode);

void USART\_IrDACmd(USART\_TypeDef\* USARTx, FunctionalState NewState);

一般常见的波特率是9600或者115200(低端的单片机如51常用9600,高端的单片机和嵌入式Coc一般用115200)。

发送端可以发送HEX文本,也可以直接发送字符文本,但无论哪种,最终发送过程都是以相应ASC码对应的十六进制数据发送的.

## I2C

1. 软件I2C,不需要用库函数,只需要配置GPIO口,需要把SCL和SDA都输出化为开漏输出模式,并把SCL和SDA置高电平;配置硬件I2C,对应GPIO口就要配置成复用开漏输出模式,在此模式下,输出仍然有效
1. 库函数:
void I2C\_DeInit();

void I2C\_Init();

void I2C\_StructInit();

void I2C\_Cmd();

void I2C\_GenerateSTART();置1产生起始条件

void I2C\_GenerateSTOP();置1产生终止条件

void I2C\_AcknowledgeConfig();配置CR1的ACK

void I2C\_SendData();把数据写入DR寄存器

uint8\_t I2C\_ReceiveData();读取DR寄存器

void I2C\_Send7bitAddress();发送7位地址

FlagStatus I2C\_GetFlagStatus();判断标志位

ErrorStatus I2C\_CheckEvent();判断标志位

void I2C\_ClearFlag();

ITStatus I2C\_GetITStatus();读取中断标志位

void I2C\_ClearITPendingBit();清除中断标志位

void I2C\_DMACmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_DMALastTransferCmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_OwnAddress2Config(I2C\_TypeDef\* I2Cx, uint8\_t Address);

void I2C\_DualAddressCmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_GeneralCallCmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_ITConfig(I2C\_TypeDef\* I2Cx, uint16\_t I2C\_IT, FunctionalState NewState);

uint16\_t I2C\_ReadRegister(I2C\_TypeDef\* I2Cx, uint8\_t I2C\_Register);

void I2C\_SoftwareResetCmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_NACKPositionConfig(I2C\_TypeDef\* I2Cx, uint16\_t I2C\_NACKPosition);

void I2C\_SMBusAlertConfig(I2C\_TypeDef\* I2Cx, uint16\_t I2C\_SMBusAlert);

void I2C\_TransmitPEC(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_PECPositionConfig(I2C\_TypeDef\* I2Cx, uint16\_t I2C\_PECPosition);

void I2C\_CalculatePEC(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

uint8\_t I2C\_GetPEC(I2C\_TypeDef\* I2Cx);

void I2C\_ARPCmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_StretchClockCmd(I2C\_TypeDef\* I2Cx, FunctionalState NewState);

void I2C\_FastModeDutyCycleConfig(I2C\_TypeDef\* I2Cx, uint16\_t I2C\_DutyCycle);

uint32\_t I2C\_GetLastEvent(I2C\_TypeDef\* I2Cx);

1. EV8\_1事件自动完成,不需要写
1. 写入DR寄存器,立即就自动将DR寄存器移入移位寄存器
## SPI

1. SS线是低电平有效,主机输出,从机输入.当SS为1时,从机的MISO引脚须切换为高阻态
1. SPI的通信尽量用高位先行
1. S1是APB2的资源,SPI2是APB1的资源
1. SPI的NSS引脚是PA4,但实际中其实可以用软件实现,因此引脚可以任选;功能是:一般SPI的从机的片选端(CS)为低电平时,从机被选中,此时从机才能正常工作,此处的CS便是NSS引脚.
1. 库函数:
void SPI\_I2S\_DeInit();

void SPI\_Init();

void I2S\_Init();

void SPI\_StructInit();

void I2S\_StructInit();

void SPI\_Cmd();

void I2S\_Cmd();

void SPI\_I2S\_ITConfig();

void SPI\_I2S\_DMACmd();

void SPI\_I2S\_SendData();    写DR数据寄存器

uint16\_t SPI\_I2S\_ReceiveData();    读DR数据寄存器

void SPI\_NSSInternalSoftwareConfig();        NSS引脚配置

FlagStatus SPI\_I2S\_GetFlagStatus();获取YXE,RXNE标志位的状态

void SPI\_I2S\_ClearFlag();

ITStatus SPI\_I2S\_GetITStatus();

void SPI\_I2S\_ClearITPendingBit();

void SPI\_SSOutputCmd(SPI\_TypeDef\* SPIx, FunctionalState NewState);

void SPI\_DataSizeConfig();        8位或16位数据帧的配置

void SPI\_TransmitCRC(SPI\_TypeDef\* SPIx);

void SPI\_CalculateCRC(SPI\_TypeDef\* SPIx, FunctionalState NewState);

uint16\_t SPI\_GetCRC(SPI\_TypeDef\* SPIx, uint8\_t SPI\_CRC);

uint16\_t SPI\_GetCRCPolynomial(SPI\_TypeDef\* SPIx);

void SPI\_BiDirectionalLineConfig(SPI\_TypeDef\* SPIx, uint16\_t SPI\_Direction);

## BKP

1. BKP相关库函数:
void BKP\_DeInit();        实现数据清0

void BKP\_TamperPinLevelConfig();        配置高低电平触发Tamper

void BKP\_TamperPinCmd();    使能Tamper

void BKP\_ITConfig();

void BKP\_RTCOutputConfig();        时钟输出功能

void BKP\_SetRTCCalibrationValue();        写入RTC校准寄存器

void BKP\_WriteBackupRegister();        写备份寄存器

uint16\_t BKP\_ReadBackupRegister();        读备份寄存器

FlagStatus BKP\_GetFlagStatus();

void BKP\_ClearFlag();

ITStatus BKP\_GetITStatus();

void BKP\_ClearITPendingBit();

void PWR\_BackupAccessCmd();        设置PWR\_CR的DBP位,使能对BKP和RTC的访问

## RTC

库函数:

void RCC\_LSEConfig();    配置LSE外部低速时钟

void RCC\_LSICmd();    配置LSI内部低速时钟

void RCC\_RTCCLKConfig();    选择RTCCLK的时钟源

void RCC\_RTCCLKCmd();        启动RTC CLK

FlagStatus RCC\_GetFlagStatus();        获取RCC时钟启动的标志位

void RTC\_ITConfig();

void RTC\_EnterConfigMode();    通过设置CNF位进入配置模式

void RTC\_ExitConfigMode();        清零CNF,退出配置模式

uint32\_t  RTC\_GetCounter();    读取时钟\\获取CNT的值

void RTC\_SetCounter();            写入时间\\写入CNT

void RTC\_SetPrescaler();            配置预分频器的分频系数

void RTC\_SetAlarm();            配置闹钟

uint32\_t  RTC\_GetDivider();        读取余数寄存器

void RTC\_WaitForLastTask();        等待上次操作完成\\等待标志位RTOFF为1

void RTC\_WaitForSynchro();        等待同步\\等待RSF置1

FlagStatus RTC\_GetFlagStatus();

void RTC\_ClearFlag();

ITStatus RTC\_GetITStatus();

void RTC\_ClearITPendingBit();

1. RTC\_SetAlarm();该寄存器是只写的,不可读
## PWR

1.执行WFI\\WFE后,默认SLEEPDEEP = 0,SLEEPONEXIT = 0,即睡眠模式,立刻睡眠.如果要改这俩参数,要用操作配置寄存器的方法

Eg:SCB->SCR = 0x.....;

1. 库函数:
void PWR\_DeInit();

void PWR\_BackupAccessCmd();    使能后备区域的访问

void PWR\_PVDCmd();        使能PVD

void PWR\_PVDLevelConfig();        配置PVD的阈值电压

void PWR\_WakeUpPinCmd();        使能PA0的WAKEUP引脚,该函数不需要配合GPIO的初始化,                            高电平唤醒

void PWR\_EnterSTOPMode();        进入停止模式,第一个参数配置电压调节器,第二个参数配置                            WFI或WFE开启

void PWR\_EnterSTANDBYMode();        进入待机模式

FlagStatus PWR\_GetFlagStatus();

void PWR\_ClearFlag();

1. PWR的时钟在APB1总线
1. 停止模式开启后,退出停止模式时要调用SYSTEM\_INIT函数来重新配置系统时钟,而待机模式就不需要,因为待机模式会从头开始运行程序
1. 待机模式之后的代码执行不到
1. 待机模式代码之前,要尽量把外挂外设关闭,不然就不会省电了.
## 看门狗

1. 独立看门狗库函数:
void IWDG\_WriteAccessCmd();键寄存器写使能

void IWDG\_SetPrescaler();写入预分频器

void IWDG\_SetReload();写重装值

void IWDG\_ReloadCounter();喂狗

void IWDG\_Enable();

FlagStatus IWDG\_GetFlagStatus();

FlagStatus RCC\_GetFlagStatus();查看RCC标志位(看复位是由何种功能引起)

void RCC\_ClearFlag();

1. 窗口看门狗的库函数:
void WWDG\_DeInit();

void WWDG\_SetPrescaler();

void WWDG\_SetWindowValue();写入窗口值

void WWDG\_EnableIT();

void WWDG\_SetCounter( );写入计数器\\喂狗

void WWDG\_Enable(); 参数是喂狗值

FlagStatus WWDG\_GetFlagStatus();

void WWDG\_ClearFlag();