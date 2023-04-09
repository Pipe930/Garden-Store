export interface Product {
  id: number;
  name_product: string;
  price: number;
  stock: number;
  image: string;
  slug: string;
  description: string;
  condition: boolean;
  create: string;
  idCategory: number;
  idOffer: number;
}

export interface ResponseProducts {
  count: number;
  next?: string;
  previous?: string;
  results: Array<Product>;
}
