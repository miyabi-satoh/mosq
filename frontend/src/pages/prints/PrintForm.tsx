import {
  Box,
  Button,
  FormControl,
  FormHelperText,
  Grid,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@material-ui/core";
import { useEffect, useState } from "react";
import { Controller, SubmitHandler, useForm, useWatch } from "react-hook-form";
import { useHistory, useParams } from "react-router-dom";
import {
  apiMaster,
  apiPrints,
  TGrade,
  TPrintDetail,
  TPrintHead,
  TPrintType,
  TUnit,
} from "api";
import { Indicator, RouterButton, RouterLink } from "components";
import { useAuth } from "contexts/Auth";
import { Alert } from "@material-ui/lab";

interface IFormInput {
  title: string;
  description: string;
  password: string;
  printtype: string;
  details: {
    unit: number;
    quantity: number;
  }[];
  question_count: number;
}
type TFormError = {
  [P in keyof IFormInput]?: string[];
};

const backUrl = `/prints`;

function PrintForm() {
  const { currentUser } = useAuth();
  const history = useHistory();
  const { printId } = useParams<{ printId: string }>();
  const [fetchError, setFetchError] = useState<boolean | undefined>(undefined);
  const [postErrors, setPostErrors] = useState<TFormError | undefined>(
    undefined
  );
  const [unitList, setUnitList] = useState<TUnit[]>([]);
  const [printTypeList, setPrintTypeList] = useState<TPrintType[]>([]);
  const {
    register,
    control,
    handleSubmit,
    getValues,
    setValue,
    formState: { errors },
  } = useForm<IFormInput>();
  const questionCount = useWatch({
    control,
    name: "question_count",
    defaultValue: 0,
  });

  const onSubmit: SubmitHandler<IFormInput> = async (formData) => {
    const params = {
      title: formData.title,
      description: formData.description,
      password: formData.password,
      printtype: formData.printtype,
      details: formData.details.filter((d) => d.quantity > 0),
    };
    console.log(params);
    try {
      const data = printId
        ? await apiPrints.update(printId, params)
        : await apiPrints.create(params);
      console.log(data);
      history.push(backUrl);
    } catch (error) {
      if (error.response?.status === 400) {
        setPostErrors(error.response.data);
      }
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const details = getValues("details");
    const question_count = details.reduce((prev: number, current) => {
      const value: number = current.quantity;
      return isNaN(value) ? prev : Number(prev) + Number(value);
    }, 0);
    setValue("question_count", question_count);
  };

  useEffect(() => {
    let unmounted = false;
    const f = async () => {
      let _unitList: TUnit[] = [];
      let _printTypeList: TPrintType[] = [];
      let _fetchData: TPrintHead | undefined = undefined;
      try {
        _unitList = await apiMaster.units();
        _printTypeList = await apiMaster.printtypes();
        if (printId) {
          _fetchData = await apiPrints.get(printId);
          console.log(_fetchData);
        }
      } catch (error) {}

      if (!unmounted) {
        setUnitList(_unitList);
        setPrintTypeList(_printTypeList);
        setValue("title", _fetchData?.title || "");
        setValue("description", _fetchData?.description || "");
        setValue("password", _fetchData?.password || "");
        setValue("printtype", `${_fetchData?.printtype?.id || ""}`);
        let question_count = 0;
        _fetchData?.details.map((detail: TPrintDetail) => {
          _unitList.map((unit: TUnit, i: number) => {
            if (detail.unit.id === unit.id) {
              setValue(`details.${i}.unit`, unit.id!);
              setValue(`details.${i}.quantity`, detail.quantity);
              question_count += detail.quantity;
            }
            return false;
          });
          return false;
        });
        setValue("question_count", question_count);
        setFetchError(printId !== undefined && _fetchData === undefined);
      }
    };
    f();

    const cleanup = () => {
      unmounted = true;
    };
    return cleanup;
  }, [setValue, printId]);

  if (!currentUser) {
    return (
      <>
        <Alert severity="error">ログインが必要です。</Alert>
        <RouterLink to={backUrl}>戻る</RouterLink>
      </>
    );
  }

  if (fetchError === undefined) {
    return <Indicator />;
  }

  if (fetchError) {
    return (
      <>
        <Alert severity="error">プリントデータが存在しません。</Alert>
        <RouterLink to={backUrl}>戻る</RouterLink>
      </>
    );
  }

  // console.log(errors);

  return (
    <form noValidate onSubmit={handleSubmit(onSubmit)}>
      <input
        style={{ display: "none" }}
        {...register("question_count")}
        type="number"
      />
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12}>
          <Typography component="h2" variant="h6">
            プリント定義の{printId ? "編集" : "追加"}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <TextField
            size="small"
            inputProps={{
              ...register("title", {
                required: "入力必須です。",
                maxLength: {
                  value: 100,
                  message: "100文字以内で入力してください。",
                },
              }),
            }}
            label="プリントのタイトル"
            error={!!errors.title}
            helperText={
              errors.title?.message ||
              "プリントのヘッダーに印字するテキストを入力してください。"
            }
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl variant="outlined" size="small" fullWidth>
            <InputLabel id="printtype-label">プリントの形式</InputLabel>
            <Controller
              render={({ field }) => (
                <Select
                  {...field}
                  labelId="printtype-label"
                  label="プリントの形式"
                >
                  {printTypeList.map((printType) => {
                    return (
                      <MenuItem
                        key={`printtype-${printType.id}`}
                        value={printType.id}
                      >
                        {printType.type_text}
                      </MenuItem>
                    );
                  })}
                </Select>
              )}
              control={control}
              name="printtype"
              rules={{
                required: "選択必須です。",
              }}
            />
            <FormHelperText>
              {errors.printtype?.message ||
                `プリントの形式(フォーマット)を選択してください。`}
            </FormHelperText>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            size="small"
            type="password"
            inputProps={{
              ...register("password", {
                minLength: {
                  value: 4,
                  message: `4〜32文字で入力してください。`,
                },
                maxLength: {
                  value: 32,
                  message: `4〜32文字で入力してください。`,
                },
              }),
            }}
            label="パスワード"
            error={!!errors.password}
            helperText={
              errors.password?.message ||
              "設定すると更新・削除でパスワードを要求します。(4〜32文字)"
            }
            fullWidth
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            size="small"
            inputProps={{
              ...register("description", {
                maxLength: {
                  value: 100,
                  message: `100文字以内で入力してください。`,
                },
              }),
            }}
            label="説明"
            error={!!errors.description}
            helperText={
              errors.description?.message ||
              "説明があれば入力してください。(プリントには印字されません)"
            }
            fullWidth
          />
        </Grid>
        <Grid item xs={12}>
          <Typography variant="subtitle2">単元ごとの問題数</Typography>
        </Grid>
        {unitList.map((unit: TUnit, i: number) => {
          const grade = unit.grade as TGrade;
          return (
            <Grid item xs={12} sm={6} md={4} key={`unit-${i}`}>
              <Box display="flex" alignItems="center">
                <TextField
                  size="small"
                  type="number"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        {`${grade.grade_text}:${unit.unit_text}(${unit.question_count})`}
                      </InputAdornment>
                    ),
                  }}
                  inputProps={{
                    ...register(`details.${i}.quantity`, {
                      min: {
                        value: 0,
                        message: `0〜${unit.question_count}の範囲で入力してください。`,
                      },
                      max: {
                        value: unit.question_count!,
                        message: `0〜${unit.question_count}の範囲で入力してください。`,
                      },
                    }),
                    min: 0,
                    max: unit.question_count,
                    style: { textAlign: "right" },
                  }}
                  onChange={handleChange}
                  disabled={unit.question_count === 0}
                  fullWidth
                />
              </Box>
            </Grid>
          );
        })}
        {postErrors && (
          <Grid item xs={12}>
            <Alert severity="error">エラーがあります。</Alert>
          </Grid>
        )}
        <Grid item xs={12} sm={4}>
          <Box textAlign="center">全 {questionCount} 問</Box>
        </Grid>
        <Grid item xs={6} sm={4}>
          <RouterButton
            fullWidth
            variant="contained"
            color="primary"
            to={backUrl}
          >
            キャンセル
          </RouterButton>
        </Grid>
        <Grid item xs={6} sm={4}>
          <Button fullWidth variant="contained" color="secondary" type="submit">
            保存
          </Button>
        </Grid>
      </Grid>
    </form>
  );
}

export default PrintForm;
