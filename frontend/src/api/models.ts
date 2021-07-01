type TModelBase = {
  id?: number;
};

export type TUser = TModelBase & {
  username: string;
};

export type TGrade = TModelBase & {
  grade_code: string;
  grade_text: string;
};

export type TUnit = TModelBase & {
  unit_code: string;
  unit_text: string;
  question_count?: number;
  grade: TGrade;
};

export type TPrintType = TModelBase & {
  type_text: string;
};

export type TPrintDetail = TModelBase & {
  unit: TUnit;
  quantity: number;
};

export type TPrintHead = TModelBase & {
  title: string;
  description: string;
  password: string;
  details: TPrintDetail[];
  archives: TArchive[];
  printtype: TPrintType;
};

export type TArchive = TModelBase & {
  file: string;
  title: string;
  created_at: Date;
  printhead: number;
};
