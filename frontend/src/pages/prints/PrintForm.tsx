import {
  Box,
  Button,
  createStyles,
  FormControl,
  FormHelperText,
  Grid,
  IconButton,
  InputLabel,
  makeStyles,
  MenuItem,
  OutlinedInput,
  Select,
  TextField,
  Theme,
  Typography,
} from "@material-ui/core";
import { useEffect, useState } from "react";
import { Controller, useFieldArray, useForm, useWatch } from "react-hook-form";
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
import { AddCircle, RemoveCircle } from "@material-ui/icons";
import { logger } from "helper";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    inputQuantity: {
      width: 120,
      minWidth: 120,
      marginRight: theme.spacing(1),
    },
    selectUnits: {
      flexGrow: 1,
    },
    iconRemove: {
      marginTop: 5,
    },
  })
);

type TFormValues = {
  title: string;
  description: string;
  printtype: number | "";
  details: {
    units: number[];
    quantity: number;
  }[];
  question_count: number;
};

type TPostErrors = {
  [P in keyof TFormValues]?: string[];
};

const backUrl = `/prints`;

function PrintForm() {
  const classes = useStyles();
  const { currentUser } = useAuth();
  const history = useHistory();
  const { printId } = useParams<{ printId: string }>();
  const [fetchError, setFetchError] = useState<boolean | undefined>(undefined);
  const [postErrors, setPostErrors] = useState<TPostErrors | undefined>(
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
  } = useForm<TFormValues>();
  const { fields, append, remove } = useFieldArray({
    control,
    name: "details",
  });
  const questionCount = useWatch({
    control,
    name: "question_count",
    defaultValue: 0,
  });

  const onSubmit = async (formData: TFormValues) => {
    setPostErrors(undefined);
    const params = {
      title: formData.title,
      description: formData.description,
      // password: formData.password,
      printtype: formData.printtype,
      details: formData.details.filter((d) => d.quantity > 0),
    };
    logger(params);
    try {
      const data = printId
        ? await apiPrints.update(printId, params)
        : await apiPrints.create(params);
      logger(data);
      history.push(backUrl);
    } catch (error) {
      if (error.response?.status === 400) {
        setPostErrors(error.response.data);
      }
    }
  };

  const handleChange = () => {
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
          logger(_fetchData);
        }
      } catch (error) {}

      if (!unmounted) {
        setUnitList(_unitList);
        setPrintTypeList(_printTypeList);
        setValue("title", _fetchData?.title || "");
        setValue("description", _fetchData?.description || "");
        // setValue("password", _fetchData?.password || "");
        setValue("printtype", _fetchData?.printtype?.id || "");
        let question_count = 0;
        if (!!_fetchData) {
          append(
            _fetchData?.details.map((detail: TPrintDetail, index) => {
              const units = detail.units.map((u) => u.id) as number[];
              question_count += detail.quantity;
              return {
                units,
                quantity: detail.quantity,
              };
            })
          );
        }
        setValue("question_count", question_count);
        setFetchError(printId !== undefined && _fetchData === undefined);
      }
    };
    f();

    const cleanup = () => {
      unmounted = true;
    };
    return cleanup;
  }, [setValue, append, printId]);

  if (fetchError === undefined) {
    return <Indicator />;
  }

  if (!currentUser) {
    return (
      <>
        <Alert severity="error">ログインが必要です。</Alert>
        <RouterLink to={backUrl}>戻る</RouterLink>
      </>
    );
  }

  if (fetchError) {
    return (
      <>
        <Alert severity="error">プリントデータが存在しません。</Alert>
        <RouterLink to={backUrl}>戻る</RouterLink>
      </>
    );
  }

  if (!!errors) {
    logger(errors);
  }
  if (!!postErrors) {
    logger(postErrors);
  }

  return (
    <form noValidate onSubmit={handleSubmit(onSubmit)}>
      <input
        style={{ display: "none" }}
        {...register("question_count", {
          min: {
            value: 1,
            message: "問題数を指定してください。",
          },
        })}
        type="number"
      />
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12}>
          <Typography component="h2" variant="h6">
            プリント定義の{printId ? "編集" : "追加"}
          </Typography>
        </Grid>
        <Grid item container spacing={2} alignItems="flex-start">
          <Grid item xs={12} md={6}>
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
              label="タイトル"
              error={!!errors.title}
              helperText={errors.title?.message}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl variant="outlined" size="small" fullWidth>
              <InputLabel id="printtype-label">形式</InputLabel>
              <Controller
                render={({ field }) => (
                  <Select
                    {...field}
                    labelId="printtype-label"
                    label="形式"
                    error={!!errors.printtype}
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
              <FormHelperText error>{errors.printtype?.message}</FormHelperText>
            </FormControl>
          </Grid>
        </Grid>
        {/* <Grid item xs={12} md={6}>
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
        </Grid> */}
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
            helperText={errors.description?.message}
            fullWidth
          />
        </Grid>
        <Grid item xs={12}>
          <Typography variant="subtitle2">出題設定</Typography>
          <FormHelperText error>
            {errors.question_count?.message}
          </FormHelperText>
        </Grid>
        {fields.map((fieldItem, index) => {
          return (
            <Grid item xs={12} key={fieldItem.id}>
              <Box display="flex" alignItems="flex-start">
                <TextField
                  size="small"
                  type="number"
                  inputProps={{
                    ...register(`details.${index}.quantity` as const, {
                      required: "入力必須です。",
                      min: {
                        value: 1,
                        message: "不正な値です。",
                      },
                    }),
                    min: 1,
                    style: { textAlign: "right" },
                  }}
                  defaultValue={fieldItem.quantity}
                  label="問題数"
                  onChange={handleChange}
                  className={classes.inputQuantity}
                  error={!!errors.details?.[index]?.quantity}
                  helperText={errors.details?.[index]?.quantity?.message}
                />
                <FormControl
                  variant="outlined"
                  size="small"
                  className={classes.selectUnits}
                >
                  <InputLabel id={`details-${index}-units-label`}>
                    単元
                  </InputLabel>
                  <Controller
                    render={({ field }) => (
                      <Select
                        {...field}
                        labelId={`details-${index}-units-label`}
                        multiple
                        input={<OutlinedInput label="単元" />}
                        error={!!errors.details?.[index]?.units}
                      >
                        {unitList.map((unit) => {
                          if (unit.question_count === 0) {
                            return null;
                          }
                          const grade = unit.grade as TGrade;
                          return (
                            <MenuItem
                              key={`${fieldItem.id}-${unit.id}`}
                              value={unit.id}
                            >
                              {`${grade.grade_text}:${unit.unit_text}(${
                                unit.question_count! >= 100
                                  ? "99+"
                                  : unit.question_count
                              })`}
                            </MenuItem>
                          );
                        })}
                      </Select>
                    )}
                    control={control}
                    name={`details.${index}.units`}
                    defaultValue={fieldItem.units}
                    rules={{
                      required: "選択必須です。",
                    }}
                  />
                  <FormHelperText error>
                    {(errors.details?.[index]?.units as any)?.message}
                  </FormHelperText>
                </FormControl>
                <IconButton
                  className={classes.iconRemove}
                  size="small"
                  color="secondary"
                  onClick={() => {
                    remove(index);
                    handleChange();
                  }}
                >
                  <RemoveCircle />
                </IconButton>
              </Box>
            </Grid>
          );
        })}
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddCircle />}
            onClick={() =>
              append({
                units: [],
              })
            }
          >
            設問追加
          </Button>
        </Grid>
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
