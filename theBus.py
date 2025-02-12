import random
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def cardToNumber(card):
    value = card[0]
    if value == 'A':
        return 1
    if value in ['J', 'Q', 'K']:
        return 13
    else:
        return int(value)

#Constants
pullHistory = []
pulls = 0
freshDeck = ['2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'AH', 'KH', 'QH', 'JH',
 '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'AS', 'KS', 'QS', 'JS',
 '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'AC', 'KC', 'QC', 'JC',
 '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'AD', 'KD', 'QD', 'JD']
activeDeck = freshDeck[:]
stage = 0
stage0Card = ''
stage1Card = ''
stageSuccessCount = [0, 0, 0, 0]  # Count successes for stages 0, 1, 2, 3
totalPullsPerStage = [0, 0, 0, 0]  # Total pulls for each stage
stageCount = [0, 0, 0, 0]  # Counts for each stage

#Control
stage1Strat = 'optimal' #optimal or random
stage1Number = 7.5
stage2Strat = 'optimal' #optimal or random
iterations = 100000000
curIterations = 0


while (curIterations < iterations):

    if (stage != 4):
        if (len(activeDeck) == 0):
            activeDeck = freshDeck[:]

        deltCard = random.choice(activeDeck)
        activeDeck.remove(deltCard)
        pulls += 1

    #print(stage)

    match stage:
        case 0:

            #Red or Black

            stage0Card = deltCard

            choice = random.randrange(0,2)

            if (choice == 0 and (deltCard[1] == 'H' or deltCard[1] == 'D')) or \
               (choice == 1 and (deltCard[1] == 'S' or deltCard[1] == 'C')):
                stageSuccessCount[0] += 1
                stage += 1
            else:
                stage = 0
            stageCount[0] += 1

        case 1:

            #high/low

            stage1Card = deltCard

            if stage1Strat == 'random':
                choice = random.choice(['high', 'low'])
            else:
                value = cardToNumber(deltCard)
                if (value >= stage1Number):
                    choice = 'low'
                else:
                    choice = 'high'

            if (cardToNumber(deltCard) > cardToNumber(stage0Card) and choice == 'high') or \
               (cardToNumber(deltCard) < cardToNumber(stage0Card) and choice == 'low'):
                stageSuccessCount[1] += 1
                stage += 1
            else:
                stage = 0
            stageCount[1] += 1


        case 2:

            #In/out

            if stage1Strat == 'random':
                choice = random.choice(['in', 'out'])
            else:
                diff = abs(cardToNumber(stage0Card) - cardToNumber(stage1Card))
                if (diff > 6.5):
                    choice = 'in'
                else:
                    choice = 'out'

            if (choice == 'in' and cardToNumber(stage0Card) < cardToNumber(deltCard) < cardToNumber(stage1Card)) or \
               (choice == 'out' and (cardToNumber(deltCard) < cardToNumber(stage0Card) or cardToNumber(deltCard) > cardToNumber(stage1Card))):
                stage += 1
                stageSuccessCount[2] += 1
            else:
                stage = 0
                stageCount[2] += 1

        case 3:

            #Suit

            deltSuit = deltCard[1]

            choice = random.choice(['D', 'H', 'S', 'C'])

            if deltSuit == choice:
                stage += 1
                stageSuccessCount[3] += 1
            else:
                stage = 0
            stageCount[3] += 1

        case 4:

            #off the bus!!!

            #print(f'Got off in {pulls} cards')
            pullHistory.append(pulls)
            for i in range(4):  # Track total pulls per stage
                totalPullsPerStage[i] += pulls if stageCount[i] > 0 else 0
            pulls = 0
            activeDeck = freshDeck[:]
            stage = 0
            totalPullsPerStage[0] += pulls
            curIterations+=1
            if (curIterations%(iterations/1000) == 0):
                print(f'Iterations = {curIterations}')
        

# Calculate frequencies of pulls
pull_counts = Counter(pullHistory)
pulls = list(pull_counts.keys())
frequencies = list(pull_counts.values())

# Calculate statistics
if pullHistory:
    # Basic Statistics
    mean_pulls = np.mean(pullHistory)
    median_pulls = np.median(pullHistory)
    mode_pulls = Counter(pullHistory).most_common(1)[0][0]
    std_dev_pulls = np.std(pullHistory)

    # Frequency Distribution
    pull_counts = Counter(pullHistory)
    pulls = list(pull_counts.keys())
    frequencies = list(pull_counts.values())

    # Min and Max
    min_pulls = min(pullHistory)
    max_pulls = max(pullHistory)

    # Percentiles
    percentile_25 = np.percentile(pullHistory, 25)
    percentile_75 = np.percentile(pullHistory, 75)

    # Printing statistics
    print("Basic Statistics:")
    print(f"Mean pulls: {mean_pulls:.2f}")
    print(f"Median pulls: {median_pulls}")
    print(f"Mode pulls: {mode_pulls}")
    print(f"Standard Deviation: {std_dev_pulls:.2f}")
    print(f"Min pulls: {min_pulls}")
    print(f"Max pulls: {max_pulls}")
    print(f"25th Percentile: {percentile_25}")
    print(f"75th Percentile: {percentile_75}")

    # Stage success rates
    stage_success_rates = [success / (success + fail) * 100 if (success + fail) > 0 else 0
                           for success, fail in zip(stageSuccessCount, stageCount)]
    for i, rate in enumerate(stage_success_rates):
        print(f"Stage {i} Success Rate: {rate:.2f}%")

    # Average pulls per stage
    for i in range(4):
        # Count of total attempts in each stage
        total_attempts = stageCount[i]  # Total attempts made in stage i
        if total_attempts > 0:
            # Calculate the average only if there were attempts
            avg_pulls_per_stage = totalPullsPerStage[i] / total_attempts
        else:
            avg_pulls_per_stage = 0
        print(f"Average pulls in Stage {i}: {avg_pulls_per_stage:.2f}")

    # Pull Ratios (Higher vs. Lower Choices)
    higher_choices = sum([1 for x in pullHistory if x > 7])
    lower_choices = sum([1 for x in pullHistory if x <= 7])
    print(f"Higher Choices: {higher_choices}, Lower Choices: {lower_choices}")

# Plot frequency bar graph
plt.bar(pulls, frequencies, color="skyblue")
plt.title("Frequency of Pulls in the Game")
plt.xlabel("Number of Pulls to Get Off the Bus")
plt.ylabel("Frequency")
plt.show()