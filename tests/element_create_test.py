import os, sys
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mod_path)
import autosar
import unittest

class TestElementCreate(unittest.TestCase):

    def test_createRealType_AR3_with_infinite(self):
        ws = autosar.workspace(version="3.0.2")
        package = ws.createPackage('DataTypes')
        dataType = package.createRealDataType('float32', 'INFINITE', 'INFINITE')
        self.assertIsInstance(dataType, autosar.datatype.RealDataType)
        self.assertEqual(dataType.minVal, 'INFINITE') #for some strange reason, the creators of AUTOSAR 3 seems to think that -INFINITE and INFINITE are the same thing?
        self.assertEqual(dataType.maxVal, 'INFINITE')
        self.assertEqual(dataType.encoding, 'SINGLE')

    def test_createRealType_AR3_with_infinite_negative(self):
        ws = autosar.workspace(version="3.0.2")
        package = ws.createPackage('DataTypes')
        dataType = package.createRealDataType('float32', '-INFINITE', 'INFINITE')
        self.assertIsInstance(dataType, autosar.datatype.RealDataType)
        self.assertEqual(dataType.minVal, 'INFINITE')
        self.assertEqual(dataType.maxVal, 'INFINITE')
        self.assertEqual(dataType.encoding, 'SINGLE')

    def test_createRealType_AR3_with_inf(self):
        ws = autosar.workspace(version="3.0.2")
        package = ws.createPackage('DataTypes')
        dataType = package.createRealDataType('float32', '-INF', 'INF')
        self.assertIsInstance(dataType, autosar.datatype.RealDataType)
        self.assertEqual(dataType.minVal, 'INFINITE')
        self.assertEqual(dataType.maxVal, 'INFINITE')
        self.assertEqual(dataType.encoding, 'SINGLE')

    def test_createRealType_AR4_with_no_constraint_package_set(self):
        ws = autosar.workspace(version="4.2.2")
        basetypes = ws.createPackage('BaseTypes')
        float32_base = basetypes.createBaseType('float32', 32, 'IEEE754')
        package = ws.createPackage('DataTypes')
        with self.assertRaises(RuntimeError) as context:
            dataType = package.createRealDataType('float32', '-INFINITE', 'INFINITE', baseTypeRef = float32_base.ref)
    
    def test_createRealType_AR4_with_infinite(self):
        ws = autosar.workspace(version="4.2.2")
        constraints = ws.createPackage('Contraints', role='DataConstraint')
        basetypes = ws.createPackage('BaseTypes')
        float32_base = basetypes.createBaseType('float32', 32, 'IEEE754')
        package = ws.createPackage('DataTypes')        
        dataType = package.createRealDataType('float32', 'INFINITE', 'INFINITE', baseTypeRef = float32_base.ref)
        self.assertIsInstance(dataType, autosar.datatype.ImplementationDataType)
        dataConstraint = ws.find(dataType.variantProps[0].dataConstraintRef)
        self.assertIsInstance(dataConstraint, autosar.datatype.DataConstraint)
        self.assertEqual(dataConstraint.rules[0].lowerLimit, '-INF')
        self.assertEqual(dataConstraint.rules[0].upperLimit, 'INF')
    
    def test_createRealType_AR4_with_infinite_negative(self):
        ws = autosar.workspace(version="4.2.2")
        constraints = ws.createPackage('Contraints', role='DataConstraint')
        basetypes = ws.createPackage('BaseTypes')
        float32_base = basetypes.createBaseType('float32', 32, 'IEEE754')
        package = ws.createPackage('DataTypes')        
        dataType = package.createRealDataType('float32', '-INFINITE', 'INFINITE', baseTypeRef = float32_base.ref)
        self.assertIsInstance(dataType, autosar.datatype.ImplementationDataType)
        dataConstraint = ws.find(dataType.variantProps[0].dataConstraintRef)
        self.assertIsInstance(dataConstraint, autosar.datatype.DataConstraint)
        self.assertEqual(dataConstraint.rules[0].lowerLimit, '-INF')
        self.assertEqual(dataConstraint.rules[0].upperLimit, 'INF')
        
    def test_createRealType_AR4_with_inf(self):
        ws = autosar.workspace(version="4.2.2")
        constraints = ws.createPackage('Contraints', role='DataConstraint')
        basetypes = ws.createPackage('BaseTypes')
        float32_base = basetypes.createBaseType('float32', 32, 'IEEE754')
        package = ws.createPackage('DataTypes')        
        dataType = package.createRealDataType('float32', '-INF', 'INF', baseTypeRef = float32_base.ref)
        self.assertIsInstance(dataType, autosar.datatype.ImplementationDataType)
        dataConstraint = ws.find(dataType.variantProps[0].dataConstraintRef)
        self.assertIsInstance(dataConstraint, autosar.datatype.DataConstraint)
        self.assertEqual(dataConstraint.rules[0].lowerLimit, '-INF')
        self.assertEqual(dataConstraint.rules[0].upperLimit, 'INF')


if __name__ == '__main__':
    unittest.main()