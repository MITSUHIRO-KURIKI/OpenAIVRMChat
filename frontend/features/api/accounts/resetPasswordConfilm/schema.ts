import { z } from 'zod';
import { passwordSchema } from '../utils/schema';


export const resetPasswordConfilmFormSchema = z
  .object({
    new_password:    passwordSchema,
    re_new_password: z.string().min(1, { message: 'Please enter your password again to confirm.' }),
  })
  .refine(
    (data) => data.re_new_password === data.new_password, {
      message: 'New password and confirmation password do not match', path: ['re_new_password'],
  })

export type ResetPasswordConfilmFormInputType = z.infer<typeof resetPasswordConfilmFormSchema>;