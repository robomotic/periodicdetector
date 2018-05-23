# Tool to identify periodic behaviour in network sessions

Malware and in particular botnets needs to send a heart-beat message to their control center to signal they are available.
It is very difficult to identify such behaviour for two reasons:
* the period is not always regular e.g. it might differ from a few msec or seconds
* some events could be missing inentionally or non-intentionally (host is down, updating etc. etc.)
This python component implements an algorithm from this [paper](https://link.springer.com/article/10.1631/FITEE.1400345).

## Using the library

Please see the unit test example in test_weblogs for an example on real malware traffic.

```python
# create the object
agcd = AGCD()

try:
    # event_seconds is a list of integers (can be seconds or msec)
    # compute the histogrm of possible periods
    agcd.period_histogram(event_seconds)
    # compute the entropy distribution, default is bit
    entropy = agcd.entropy_histogram()
    # magic threshold, usually more than 4 bits is good for a high SNR
    if entropy > 4.0:
        print("Beacon detection for source = {0} and url = {1} with {2} events".format(source, url,len(event_seconds)))
        # get the period with more counts
        period_estimate = agcd.period_max()

        print("Maximum period found p = {0} ".format(period_estimate))
        print("Binary entropy = {0:.2f}".format(entropy))

except AGCDException as e:
    print(e)
```



## Requirements

* Python 3.6 or Python2.7
* requests