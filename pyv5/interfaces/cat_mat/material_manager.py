"""
Module initially auto generated using V5Automation files from CATIA V5 R28 on
2020-09-25 14:34:21.593357

.. warning::
    The notes denoted "CAA V5 Visual Basic Help" are to be used as reference only.
    They are there as a guide as to how the Visual Basic / catscript functions work
    and thus help debugging in pyv5.

"""

from pyv5.interfaces.cat_mat.material import Material
from pyv5.base.enums import CatScriptLanguage
from pyv5.interfaces.mec_mod.body import Body
from pyv5.interfaces.mec_mod.hybrid_body import HybridBody
from pyv5.interfaces.mec_mod.part import Part
from pyv5.interfaces.product_structure.product import Product
from pyv5.interfaces.system.any_object import AnyObject


class MaterialManager(AnyObject):
    """
    .. note::
        :class: toggle

        CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)

            | System.IUnknown
            |     System.IDispatch
            |         System.CATBaseUnknown
            |             System.CATBaseDispatch
            |                 System.AnyObject
            |                     MaterialManager
            |
            | Interface to manage material manager object.
            | Role: A material manager is used to manage materials application
            | on geometrical objects.

    """

    def __init__(self, com_object):
        super().__init__(com_object)
        self.material_manager = com_object

    def apply_material_on_body(
        self, i_body: Body, i_material: Material | None, i_link_mode: int = 0
    ) -> None:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub ApplyMaterialOnBody(Body iBody,
                | Material iMaterial,
                | short iLinkMode)
                |
                |     Apply a Material on a Body. If Material is NULL, deletes
                |     the material already applied on the Body.

        :param Body i_body:
        :param Material i_material:
        :param int i_link_mode:
        :rtype: None
        """
        self.material_manager.ApplyMaterialOnBody(
            i_body.com_object,
            None if i_material is None else i_material.com_object,
            i_link_mode,
        )

    def apply_material_on_hybrid_body(
        self,
        i_hybrid_body: HybridBody,
        i_material: Material | None,
        i_link_mode: int = 0,
    ) -> None:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub ApplyMaterialOnHybridBody(HybridBody iHybridBody,
                | Material iMaterial,
                | short iLinkMode)
                |
                |     Apply a Material on a Hybrid Body. If Material is NULL,
                |     deletes the material already applied on the Hybrid Body

        :param HybridBody i_hybrid_body:
        :param Material i_material:
        :param int i_link_mode:
        :rtype: None
        """
        self.material_manager.ApplyMaterialOnHybridBody(
            i_hybrid_body.com_object,
            None if i_material is None else i_material.com_object,
            i_link_mode,
        )

    def apply_material_on_part(
        self, i_part: Part, i_material: Material | None, i_link_mode: int = 0
    ) -> None:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub ApplyMaterialOnPart(Part iPart,
                | Material iMaterial,
                | short iLinkMode)
                |
                |     Apply a Material on a Part. If Material is NULL, deletes
                |     the material already applied on the Part

        :param Part i_part:
        :param Material i_material:
        :param int i_link_mode:
        :rtype: None
        """
        self.material_manager.ApplyMaterialOnPart(
            i_part.com_object,
            None if i_material is None else i_material.com_object,
            i_link_mode,
        )

    def apply_material_on_product(
        self,
        i_product: Product,
        i_material: Material | None,
        i_link_mode: int = 0,
    ) -> None:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub ApplyMaterialOnProduct(Product iProduct,
                | Material iMaterial,
                | short iLinkMode)
                |
                |     Apply a Material on a Product. If Material is NULL,
                |     deletes the material already applied on the Product

        :param Product i_product:
        :param Material i_material:
        :param int i_link_mode:
        :rtype: None
        """
        self.material_manager.ApplyMaterialOnProduct(
            i_product.com_object,
            None if i_material is None else i_material.com_object,
            i_link_mode,
        )

    def apply_material_on_user_material(
        self,
        i_user_material: AnyObject,
        i_material: Material | None,
        i_link_mode: int = 0,
    ) -> None:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub ApplyMaterialOnUserMaterial(AnyObject iUserMaterial,
                | Material iMaterial,
                | short iLinkMode)
                |
                |     Apply a Material on a User Material (Analysis entity).
                |     Warning:
                |     iUserMaterial should be a CATIAAnalysisEntity object. If
                |     Material is NULL, deletes the material already applied on
                |     the User Material

        :param AnyObject i_user_material:
        :param Material i_material:
        :param int i_link_mode:
        :rtype: None
        """
        self.material_manager.ApplyMaterialOnUserMaterial(
            i_user_material,
            None if i_material is None else i_material.com_object,
            i_link_mode,
        )

    def get_material_on_body(self, i_body: Body) -> Material:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub GetMaterialOnBody(Body iBody,
                | Material oMaterial)
                |
                |     Get a Material on a Body. Material returned is NULL if no
                |     material is applied on the Body

        :param Body i_body:
        :param Material o_material:
        :rtype: None
        """
        vba_function_name = "get_material_on_body"
        vba_code = f"""        
        Public Function {vba_function_name}(material_manager, body)
            Dim material
            material_manager.GetMaterialOnBody body, material
            Set {vba_function_name} = material
        End Function
        """
        system_service = self.application.system_service
        return Material(
            system_service.evaluate(
                vba_code,
                CatScriptLanguage.CATVBScriptLanguage,
                vba_function_name,
                [self.com_object, i_body.com_object],
            )
        )

    def get_material_on_hybrid_body(self, i_hybrid_body: HybridBody) -> Material:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub GetMaterialOnHybridBody(HybridBody iHybridBody,
                | Material oMaterial)
                |
                |     Get a Material on a Hybrid Body. Material returned is
                |     NULL if no material is applied on the Hybrid Body

        :param HybridBody i_hybrid_body:
        :param Material o_material:
        :rtype: None
        """
        vba_function_name = "get_material_on_hybrid_body"
        vba_code = f"""        
        Public Function {vba_function_name}(material_manager, hybrid_body)
            Dim material
            material_manager.GetMaterialOnHybridBody hybrid_body, material
            Set {vba_function_name} = material
        End Function
        """
        system_service = self.application.system_service
        return Material(
            system_service.evaluate(
                vba_code,
                CatScriptLanguage.CATVBScriptLanguage,
                vba_function_name,
                [self.com_object, i_hybrid_body.com_object],
            )
        )

    def get_material_on_part(self, i_part: Part) -> Material:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub GetMaterialOnPart(Part iPart,
                | Material oMaterial)
                |
                |     Get a Material on a Part. Material returned is NULL if no
                |     material is applied on the Part

        :param Part i_part:
        :param Material o_material:
        :rtype: None
        """
        vba_function_name = "get_material_on_part"
        vba_code = f"""        
        Public Function {vba_function_name}(material_manager, part)
            Dim material
            material_manager.GetMaterialOnPart part, material
            Set {vba_function_name} = material
        End Function
        """
        system_service = self.application.system_service
        return Material(
            system_service.evaluate(
                vba_code,
                CatScriptLanguage.CATVBScriptLanguage,
                vba_function_name,
                [self.com_object, i_part.com_object],
            )
        )

    def get_material_on_product(self, i_product: Product) -> Material:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub GetMaterialOnProduct(Product iProduct,
                | Material oMaterial)
                |
                |     Get a Material on a Product. Material returned is NULL if
                |     no material is applied on the Product

        :param Product i_product:
        :param Material o_material:
        :rtype: None
        """
        vba_function_name = "get_material_on_product"
        vba_code = f"""        
        Public Function {vba_function_name}(material_manager, product)
            Dim material
            material_manager.GetMaterialOnProduct product, material
            Set {vba_function_name} = material
        End Function
        """
        system_service = self.application.system_service
        return Material(
            system_service.evaluate(
                vba_code,
                CatScriptLanguage.CATVBScriptLanguage,
                vba_function_name,
                [self.com_object, i_product.com_object],
            )
        )

    def get_material_on_user_material(self, i_user_material: AnyObject) -> Material:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub GetMaterialOnUserMaterial(AnyObject iUserMaterial,
                | Material oMaterial)
                |
                |     Get a Material on a User Material (Analysis entity).
                |     Warning: iUserMaterial should be a CATIAAnalysisEntity
                |     object. Material returned is NULL if no material is
                |     applied on the User Material

        :param AnyObject i_user_material:
        :param Material o_material:
        :rtype: None
        """
        vba_function_name = "get_material_on_user_material"
        vba_code = f"""        
        Public Function {vba_function_name}(material_manager, user_material)
            Dim material
            material_manager.GetMaterialOnUserMaterial user_material, material
            Set {vba_function_name} = material
        End Function
        """
        system_service = self.application.system_service
        return Material(
            system_service.evaluate(
                vba_code,
                CatScriptLanguage.CATVBScriptLanguage,
                vba_function_name,
                [self.com_object, i_user_material.com_object],
            )
        )

    def replace_material_links(
        self, i_material1: Material, i_material2: Material
    ) -> None:
        """
        .. note::
            :class: toggle

            CAA V5 Visual Basic Help (2020-09-25 14:34:21.593357)
                | o Sub ReplaceMaterialLinks(Material iMaterial1,
                | Material iMaterial2)
                |
                |     In current session, replace all links towards a material 1
                |     with a link towards an other material 2. N.B. Both
                |     materials entered should be in a material library.

        :param Material i_material1:
        :param Material i_material2:
        :rtype: None
        """
        self.material_manager.ReplaceMaterialLinks(i_material1, i_material2)

    def __repr__(self):
        return f'MaterialManager(name="{self.name}")'
