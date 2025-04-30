import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card"
import { patch } from "@web/core/utils/patch";

patch(ProductCard, {
    props: {
        ...ProductCard.props,
        barcode: { type: undefined, optional: true },//optional:true -- means it may or may nor be required
//        lst_price:Number,
//          default_code:{type:undefined,optional:true}
          //it is sales price where field name is list_price but
          //it is not working for list_price it is working for lst_price
//           default_code:{type:undefined,optional:true},//with or without optional it is giving false without entering the value
//              if value is not given it returns false in front-end
    },


get code() {
    return this.props.barcode ?? "Empty_barcode";
    }
       } );





