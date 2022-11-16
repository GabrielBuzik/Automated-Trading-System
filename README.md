# Automated-Trading-System

This is a trend following automated strategy that has been running on a private server since 24 July 2022 with initial deposit equal 400 BUSD. The trading pair is BTCBUSD.

### Buying/Selling rules:

1. Conditions for Opening a Long position: 𝑅𝐴𝑉𝐼𝑡 (EMA(slow)=50, EMA(fast)=5)>0 when 𝑅𝐴𝑉𝐼𝑡−1(EMA(slow)=50, 
EMA(fast)=5)<0. 
2. Conditions for Closing a Long position (any):
  + 𝑉𝑡 ≤ Max (𝐴𝑇𝑅 𝑇𝑆1; 𝐴𝑇𝑅 𝑇𝑆2…𝐴𝑇𝑅 𝑇𝑆𝑡) where 𝐴𝑇𝑅 𝑇𝑆𝑖= 𝑉𝑖 - 𝐴𝑇𝑅𝑖 × 1.5 and 𝐴𝑇𝑅 𝑇𝑆1 is ATR TS at the day of Open Order
  + 𝑅𝐴𝑉𝐼𝑡−1(EMA(slow)=50, EMA(fast)=5)>2% and 𝑅𝐴𝑉𝐼𝑡(EMA(slow)=50, EMA(fast)=5) < 𝑅𝐴𝑉𝐼𝑡−1(EMA(slow)=50, EMA(fast)=5) – 0.5% and 𝑅𝐴𝑉𝐼𝑡 (EMA(slow)=50, EMA(fast)=5) < 𝑅𝐴𝑉𝐼𝑡−2(EMA(slow)=50, EMA(fast)=5) – 0.5%
  + Open a Short Position


