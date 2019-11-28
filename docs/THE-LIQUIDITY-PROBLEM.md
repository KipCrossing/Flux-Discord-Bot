# Vote Swapping via Political Capital - The Liquidity Problem

## Intro

One of the most fundamental principles that we must consider when laying out the groundwork for developing our democracy is that we strive toward equality of opportunity, in terms of voting, for everyone who is eligible. In classical democracy, this is simply done by ensuring that each person's vote has the same value and there are adequate means for them to do so. With this in mind, IBDD vote swapping via political capital (PC) presents itself with a different type of issue; how do we maintain liquidity for vote trading whilst allowing voters to accumulate PC savings?

Before starting, we must consider some practical limitations based on how issues are presented into the IBDD system. The time between submitted issues may vary significantly, and because of this we must consider two extreme cases; (1) the case where a voter waits only a short period of time before voting on an issue of interest and (2) the case where a voter needs to wait a long period of time before voting on an issue of interest. The waiting period may be considered the time that 'political capital savings' are not being used for that voter; and shall be called the "hoarding time".

There may be cases where political capital hoarding can become a problem; such that, the hoarded political capital is significantly large compared to the total volume of political capital. A case where this may occur is when a contentious issue is being voted on and the majority of the voter base decides to vote and buy votes. The few who decide to sell their vote for political capital have the potential to can make significant gains. The problems that arise are two-fold; (1) a significant proportion of the voter base would not have access to political capital and therefore are unable trade votes and (2) hoarders can hold the majority of the political capital buying power and therefore control the outcome of a vote.

### Summary

To summarise our problem, we must create a model that accounts for the following:

- (A) That democracy continues to have equality of opportunity
- (B) That liquidity of political capital is maintained so that the large majority of voters can continue to trade votes
- (C ) That the value of saved political capital does not significantly decrease over time
- (D) That hoarding of political capital does not become significantly large compared to the total volume of political capital

Before starting on the selected solution/s, some models that attempted to address the issues but failed the criteria are as followed:

- Jubilee model
- Universal Basic Income model
- Participation reward model
- Tax and redistribution model

## Inflationary model

The inflationary model consists of increasing the total volume of political capital over increments of time. It would be done by evenly distributing (passing A) new political capital to every voter (passing B). This, however, cannot be simply done arbitrarily. If the supply of new political capital is too large then the comparative value of the saved political capital would decrease significantly, leaving savers with a disadvantage due to their topic of interest having a long hoarding time (failing C). Alternatively, if the supply of new political capital is too small, compared to those with saved political capital, then there is a danger that the majority of voters may not have a significant impact on the final outcome (failing D).

So what method should be used when determining the amount of new political capital to be issued? One method is to base is on the results of the previous issue. To do this we shall use a tool called the "care factor"; a numerical representation of how much people care about an issue.

```
Care factor = (spent PC)/(total PC)
```

We could then set the new political capital (to be issued) to be equal to the care factor. If the care factor is low due to the amount of used PC being low, then the savings of the hoarders would be low and the newly issued political capital would be low (passing C and D)

But, if the care factor is high due to a high volume of spent PC, then the savings of the hoarders would increase significantly (multitudes of units)(failing D) and the newly issued political capital would increase but no larger than unity (passing C).

The problem arises because new issued political capital may be significantly smaller then gained political capital by hoarders. Therefore the new political capital needs to be proportional to the average vote price. We would then get:

```
New issued political capital = (average vote price)x(care factor)
```

Now when the new issued political capital is largely due to a high vote price, the new issued political capital is proportional to the average vote price and hence not significantly larger (Passing D). Due to the care factor, new issued political capital will not be as large as the savings made by hoarders and they can, therefore, continue to save compared to those who are spending. Note: everyone will receive the new issued political capital.

## The Human Issue

Although this model passes all of our criteria, it causes another novel, but not insignificant, issue. That is that the value of political capital will decrease due to the inflationary nature of the model. Although this wouldn't be an issue for computers, this may get confusing for some people as it would be harder to 'gauge' the value of the PC they spend each tine, over time.

To solve this, one proposal is to is to present a different unit in the UI that is calculated from their PC balance such that the value of the UI unit, per capita, is stays consistent as the total volume of PC is increased. This new balance may be calculated via:

```
UI bal = (Factor)x(PC bal)/(Total PC/number of voters)
```

Where the Factor will indicate how much of the new unit there will be per capita _for instance Factor = 100_
