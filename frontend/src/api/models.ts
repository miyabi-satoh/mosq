type TModelBase = {
  id?: number;
};

export type TGrade = TModelBase & {
  grade_code: string;
  grade_text: string;
};

export type TUnit = TModelBase & {
  unit_code: string;
  unit_text: string;
  question_count?: number;
  grade: number | TGrade;
};

export type TPrintDetail = TModelBase & {
  unit: number | TUnit;
  quantity: number;
};

export type TPrintHead = TModelBase & {
  title: string;
  details: TPrintDetail[];
};
