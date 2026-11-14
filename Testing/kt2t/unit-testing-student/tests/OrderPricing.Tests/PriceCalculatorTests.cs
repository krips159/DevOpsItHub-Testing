
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OrderPricing;

namespace OrderPricing.Tests;

[TestClass]
public class PriceCalculatorTests
{
    // R2, R4: обычный заказ без скидок
    [TestMethod]
    public void RegularOrder_1000WithoutLoyalty_TotalIs1300()
    {
        decimal subtotal = 1000m;
        decimal expected = 1300m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R3: скидка по карте
    [TestMethod]
    public void LoyaltyCard_1000_TotalIs1200()
    {
        decimal subtotal = 1000m;
        decimal expected = 1200m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    // R2: стоимость ниже порога скидки
    [TestMethod]
    public void BelowDiscountThreshold_4999_99_TotalIs5299_99()
    {
        decimal subtotal = 4999.99m;
        decimal expected = 5299.99m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R2: стоимость на пороге скидки
    [TestMethod]
    public void AtDiscountThreshold_5000_TotalIs4750()
    {
        decimal subtotal = 5000m;
        decimal expected = 4750m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R2: стоимость выше порога скидки
    [TestMethod]
    public void AboveDiscountThreshold_5000_01_TotalIs4750_01()
    {
        decimal subtotal = 5000.01m;
        decimal expected = 4750.01m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R3: карта при сумме ниже порога скидки
    [TestMethod]
    public void LoyaltyCard_BelowDiscountThreshold_TotalIs4499_99()
    {
        decimal subtotal = 4999.99m;
        decimal expected = 4499.99m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    // R3: две скидки одновременно, применяется большая
    [TestMethod]
    public void LoyaltyAndDiscount_6000_TotalIs5400()
    {
        decimal subtotal = 6000m;
        decimal expected = 5400m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    // R4: стоимость ниже порога бесплатной доставки
    [TestMethod]
    public void BelowFreeDeliveryThreshold_3999_99_TotalIs4299_99()
    {
        decimal subtotal = 3999.99m;
        decimal expected = 4299.99m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R4: стоимость на пороге бесплатной доставки
    [TestMethod]
    public void AtFreeDeliveryThreshold_4000_TotalIs4000()
    {
        decimal subtotal = 4000m;
        decimal expected = 4000m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R5: экспресс-доставка при небольшой сумме
    [TestMethod]
    public void ExpressDelivery_1000_TotalIs1500()
    {
        decimal subtotal = 1000m;
        decimal expected = 1500m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, true);

        Assert.AreEqual(expected, actual);
    }

    // R5: экспресс-доставка при большой сумме
    [TestMethod]
    public void ExpressDelivery_5000_TotalIs5250()
    {
        decimal subtotal = 5000m;
        decimal expected = 5250m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, true);

        Assert.AreEqual(expected, actual);
    }

    // R5: экспресс-доставка вместе с картой
    [TestMethod]
    public void ExpressDeliveryWithLoyalty_1000_TotalIs1400()
    {
        decimal subtotal = 1000m;
        decimal expected = 1400m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, true);

        Assert.AreEqual(expected, actual);
    }

    // R1: минимальная допустимая стоимость
    [TestMethod]
    public void Min()
    {
        decimal subtotal = 0m;
        decimal expected = 300m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R1: максимальная допустимая стоимость
    [TestMethod]
    public void Max()
    {
        decimal subtotal = 100000m;
        decimal expected = 95000m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, false, false);

        Assert.AreEqual(expected, actual);
    }

    // R1: стоимость ниже допустимого диапазона
    [TestMethod]
    public void DowngradeCost()
    {
        Assert.ThrowsException<ArgumentOutOfRangeException>(() =>
            PriceCalculator.CalculateTotal(-1m, false, false));
    }

    // R1: стоимость выше допустимого диапазона
    [TestMethod]
    public void UpgradeCost()
    {
        Assert.ThrowsException<ArgumentOutOfRangeException>(() =>
            PriceCalculator.CalculateTotal(100001m, false, false));
    }

    // R6: округление до двух знаков AwayFromZero
    [TestMethod]
    public void Rounding_100_05WithLoyalty_TotalIs390_05()
    {
        decimal subtotal = 100.05m;
        decimal expected = 390.05m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }

    // R4: бесплатная доставка определяется по исходной сумме
    [TestMethod]
    public void FreeDeliveryWithDiscount_4000WithLoyalty_TotalIs3600()
    {
        decimal subtotal = 4000m;
        decimal expected = 3600m;

        decimal actual = PriceCalculator.CalculateTotal(subtotal, true, false);

        Assert.AreEqual(expected, actual);
    }
}
