# VaR-Dollar-Yen-Exchange-Rate
Volatility Model- GARCH Model

The generalized autoregressive conditional heteroskedasticity (GARCH) models describe financial markets in which volatility can change, becoming more volatile during periods of financial crises or world events and less volatile during periods of relative calm and steady economic growth. On a plot of returns, for example, stock returns may look relatively uniform for the years leading up to a financial crisis such as that of 2007.

VaR Model- Historical Simulation with Volatility updating

Historical Simulation is a method of calculating value-at-risk (VaR) that uses historical data to assess the impact of market moves on a portfolio. A current portfolio is subjected to historically recorded market movements; this is used to generate a distribution of returns on the portfolio.

Backtesting- Binomial Test

The most straightforward test is to compare the observed number of exceptions, x, to the expected number of exceptions. From the properties of a binomial distribution, you can build a confidence interval for the expected number of exceptions. Using exact probabilities from the binomial distribution or a normal approximation, the bin function uses a normal approximation. By computing the probability of observing x exceptions, you can compute the probability of wrongly rejecting a good model when x exceptions occur. This is the p-value for the observed number of exceptions x. For a given test confidence level, a straightforward accept-or-reject result in this case is to fail the VaR model whenever x is outside the test confidence interval for the expected number of exceptions. “Outside the confidence interval” can mean too many exceptions, or too few exceptions. Too few exceptions might be a sign that the VaR model is too conservative
