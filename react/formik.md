Formik ([docs](https://jaredpalmer.com/formik/docs/tutorial)) is a small library that helps you three aspects of forms within React:

- Getting values in and out of form state
- Validation and error messages
- Handling form submission

The `Formik` component is used to wrap your form up and exposes state values and handlers via the render props.
It accepts props to set up our default values, validate the submitted values and handle our submission. The following is an example
of a form that lets you edit user data:

    import React from 'react';
    import Dialog from 'MySuperDialog';
    import { Formik, Field, Form, ErrorMessage } from 'formik';

    const EditUserDialog = ({ user, updateUser, onClose }) => {
      return (
        <Dialog onClose={onClose}>
          <h1>Edit User</h1>
          <Formik
            initialValues={user /** { email, social } */}
            onSubmit={(values, actions) => {
              MyImaginaryRestApiCall(user.id, values).then(
                updatedUser => {
                  actions.setSubmitting(false);
                  updateUser(updatedUser);
                  onClose();
                },
                error => {
                  actions.setSubmitting(false);
                  actions.setErrors(transformMyRestApiErrorsToAnObject(error));
                  actions.setStatus({ msg: 'Set some arbitrary status or data' });
                }
              );
            }}
            render={({ errors, status, touched, isSubmitting }) => (
              <Form>
                <Field type="email" name="email" />
                <ErrorMessage name="email" component="div" />
                <Field type="text" className="error" name="social.facebook" />
                <ErrorMessage name="social.facebook">
                  {errorMessage => <div className="error">{errorMessage}</div>}
                </ErrorMessage>
                <Field type="text" name="social.twitter" />
                <ErrorMessage name="social.twitter" className="error" component="div"/>
                {status && status.msg && <div>{status.msg}</div>}
                <button type="submit" disabled={isSubmitting}>
                  Submit
                </button>
              </Form>
            )}
          />
        </Dialog>
      );
    };

Formik’s render property exposes event handlers to manage changes to your form inputs, whether or not
they have been “touched”, their values and any errors. For the form as a whole, you will be able to tell if the form
is in the process of being validated or submitted and an event handler that lets you easily reset the form.

`props.values` and `props.errors` correspond with your form fields. `props.handleChange` and `props.handleBlur` can be
passed to `onChange` and `onBlur` to track changes and whether or not an input has been “touched”. This “touched” value
comes in handy when you only want to show errors after a user has interacted with an element (not when page loads).
`props.isValidating` and `props.isSubmitting` let you know what stage of the process the user is in, useful for
 displaying a loader or disabling the form or individual buttons.

The `Form` component is a small wrapper around a `form` element that automatically wires up things like the `onSubmit` handler.

    <Form />
    // is identical to this...
    <form onReset={formikProps.handleReset} onSubmit={formikProps.handleSubmit} {...props} />

**Validation**

There are 2 ways to do form-level validation with Formik:

    <Formik validate>
    <Formik validationSchema>

Using `validate`:

    const validate = (values, props /* only available when using withFormik */) => {
      let errors = {};

      if (!values.email) {
        errors.email = 'Required';
      } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
        errors.email = 'Invalid email address';
      }

      //...

      return errors;
    };

Using `validationSchema`:

    import * as Yup from 'yup';

    const SignupSchema = Yup.object().shape({
      firstName: Yup.string()
        .min(2, 'Too Short!')
        .max(50, 'Too Long!')
        .required('Required'),
      lastName: Yup.string()
        .min(2, 'Too Short!')
        .max(50, 'Too Long!')
        .required('Required'),
      email: Yup.string()
        .email('Invalid email')
        .required('Required'),
    });

    export const ValidationSchemaExample = () => (
      <div>
        <h1>Signup</h1>
        <Formik
          initialValues={{
            firstName: '',
            lastName: '',
            email: '',
          }}
          validationSchema={SignupSchema}
          onSubmit={values => {
            // same shape as initial values
            console.log(values);
          }}
        >
          {({ errors, touched }) => (
            <Form>
              <Field name="firstName" />
              {errors.firstName && touched.firstName ? (
                <div>{errors.firstName}</div>
              ) : null}
              <Field name="lastName" />
              {errors.lastName && touched.lastName ? (
                <div>{errors.lastName}</div>
              ) : null}
              <Field name="email" type="email" />
              {errors.email && touched.email ? <div>{errors.email}</div> : null}
              <button type="submit">Submit</button>
            </Form>
          )}
        </Formik>
      </div>
    );

Validation is left up to you, you can write your own validators or use a 3rd party library.
Formik has a special config option / prop for Yup called `validationSchema` which automatically transforms Yup's
validation errors into an object whose keys match `values` and `touched`.

Formik supports field-level validation via the `<Field>` components' `validate` prop. 
It will run after any `onChange` and `onBlur` by default.

    function validateEmail(value) {
      let error;
      if (!value) {
        error = 'Required';
      } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)) {
        error = 'Invalid email address';
      }
      return error;
    }

    function validateUsername(value) {
      let error;
      if (value === 'admin') {
        error = 'Nice try!';
      }
      return error;
    }

    export const FieldLevelValidationExample = () => (
      <div>
        <h1>Signup</h1>
        <Formik
          initialValues={{
            username: '',
            email: '',
          }}
          onSubmit={values => {console.log(values)}}
        >
          {({ errors, touched, isValidating }) => (
            <Form>
              <Field name="email" validate={validateEmail} />
              {errors.email && touched.email && <div>{errors.email}</div>}

              <Field name="username" validate={validateUsername} />
              {errors.username && touched.username && <div>{errors.username}</div>}

              <button type="submit">Submit</button>
            </Form>
          )}
        </Formik>
      </div>
    );
